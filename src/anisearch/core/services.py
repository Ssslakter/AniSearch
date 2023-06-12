from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from langchain.docstore.document import Document
from src.features.document_builder import DocumentBuilder
from src.anisearch.configs import Config
from src.anisearch.core.storage import Storage
from src.anisearch.data_models import AnimeData


class Services:
    """Class that holds all services"""

    def __init__(self, config: Config) -> None:
        self.embeddings = self._get_embeddings(config.models_dir)
        self.config = config
        self.document_builder = DocumentBuilder()
        self.storage = Storage(self.embeddings, self.config.qdrant)

    @staticmethod
    def _get_embeddings(models_dir: str) -> HuggingFaceEmbeddings:
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

    def initialize(self):
        """Perform some init configurations like creating collections, etc."""
        self.storage.init_collection(self.config.qdrant.collection_name)

    def insert_anime(self, anime: AnimeData):
        """Inserts anime into storage"""
        rendered = self.document_builder.render_document(anime)
        return self.storage.qdrant.add_documents(
            [
                Document(
                    page_content=rendered,
                    metadata={"anime_id": anime.anime_id, "img_url": anime.img_url},
                )
            ]
        )

    def get_collections(self):
        return self.storage.client.get_collections()
