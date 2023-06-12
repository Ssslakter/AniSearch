from qdrant_client import QdrantClient
from qdrant_client.http.exceptions import UnexpectedResponse
import qdrant_client.http.models as rest
from langchain.vectorstores import Qdrant
from langchain.embeddings.base import Embeddings

from src.anisearch.configs import QdrantConfig


class Storage:
    """Client wrapper to qdrant vector storage"""

    def __init__(self, embeddings: Embeddings, config: QdrantConfig) -> None:
        self.config = config
        self.embeddings = embeddings
        self.client = QdrantClient(url=config.url, api_key=config.api_key, timeout=100)
        self.qdrant = Qdrant(
            client=self.client,
            collection_name=config.collection_name,
            embeddings=embeddings,
        )

    def init_collection(self, collection_name: str):
        """Tries to create collection, even if it already exists

        Raises:
            err_response: If qdrant returned error response not related with existance of collection
        """
        vector_length = len(self.embeddings.embed_documents([""])[0])
        try:
            self.client.create_collection(
                collection_name,
                rest.VectorParams(
                    size=vector_length,
                    distance=rest.Distance[self.config.distance_func.upper()],
                ),
            )
        except UnexpectedResponse as err_response:
            if b"already exists!" in err_response.content:
                return
            raise err_response
