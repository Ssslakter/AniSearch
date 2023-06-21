from qdrant_client.models import Filter, FieldCondition, MatchValue, Range
from langchain.docstore.document import Document
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from src.features.document_builder import DocumentBuilder
from src.anisearch.configs import Config
from src.anisearch.core.storage import Storage
from src.anisearch.data_models import AnimeData


class Services:
    """Class that holds all services"""

    filters = (
        Filter(
            must=[
                FieldCondition(
                    key="metadata.score",
                    range=Range(gt=4.5),
                ),
                FieldCondition(
                    key="metadata.popularity",
                    range=Range(lt=8000),
                ),
            ]
        ),
    )

    def __init__(self, config: Config) -> None:
        self.embeddings = get_embeddings(config.models_dir)
        self.config = config
        self.document_builder = DocumentBuilder()
        self.storage = Storage(self.embeddings, self.config.qdrant)

    def initialize(self):
        """Perform some init configurations like creating collections, etc."""
        self.storage.init_collection(self.config.qdrant.collection_name)

    def insert_anime(self, anime: AnimeData) -> list[str]:
        """Inserts anime into storage"""
        doc = self.document_builder.render_document(anime)
        return self.storage.qdrant.add_documents([doc])

    async def search_anime(self, query: str) -> list[Document]:
        docs = await self.storage.qdrant.asearch(
            query, search_type="similarity", k=150, query_filter=Services.filters
        )
        return self.postprocess(docs)

    @staticmethod
    def _get_synopsis(doc: Document) -> Document:
        line = "Synopsis: "
        idx = doc.page_content.find(line)
        doc.page_content = doc.page_content[idx + len(line) :]
        return doc

    @staticmethod
    def postprocess(docs: list[Document]) -> list[Document]:
        docs = sorted(docs, key=lambda x: x.metadata["popularity"])[:15]
        # docs = sorted(docs, key=lambda x: x.metadata["score"], reverse=True)
        return list(map(Services._get_synopsis, docs))

    def delete_anime(self, uid: int):
        self.storage.qdrant.client.delete(
            self.config.qdrant.collection_name,
            points_selector=Filter(
                should=[FieldCondition(key="metadata.uid", match=MatchValue(value=uid))]
            ),
        )

    def get_anime(self, uid: int):
        return self.storage.qdrant.client.search(
            self.config.qdrant.collection_name,
            self.embeddings.embed_documents([""])[0],
            query_filter=Filter(
                should=[FieldCondition(key="metadata.uid", match=MatchValue(value=uid))]
            ),
        )

    def get_collections(self):
        return self.storage.client.get_collections()


def get_embeddings(models_dir: str) -> HuggingFaceEmbeddings:
    """Get default huggingface embeddings from models directory"""

    model_name = "sentence-transformers/all-mpnet-base-v2"
    model_kwargs = {"device": "cuda"}
    encode_kwargs = {"normalize_embeddings": False}
    return HuggingFaceEmbeddings(
        model_name=model_name,
        cache_folder=models_dir,
        model_kwargs=model_kwargs,
        encode_kwargs=encode_kwargs,
    )
