# from pinecone import Pinecone, ServerlessSpec
# from langchain_openai import OpenAIEmbeddings
# from langchain_pinecone import PineconeVectorStore
# from app.core.config import settings
# import logging

# logger = logging.getLogger(__name__)

# class VectorStoreService:
#     def __init__(self):
#         try:
#             self.pc = Pinecone(api_key=settings.PINECONE_API_KEY)
#             self.index_name = "ai-agent-memory"

#             # Create index if doesn't exist
#             if self.index_name not in self.pc.list_indexes().names():
#                 self.pc.create_index(
#                     name=self.index_name,
#                     dimension=1536,
#                     metric="cosine",
#                     spec=ServerlessSpec(
#                         cloud="aws",
#                         region=settings.PINECONE_ENVIRONMENT
#                     )
#                 )

#             self.embeddings = OpenAIEmbeddings(
#                 openai_api_base="https://openrouter.ai/api/v1",
#                 openai_api_key=settings.OPENROUTER_API_KEY,
#                 model="openai/text-embedding-3-small",
#                 max_tokens=1000
#             )

#             self.vector_store = PineconeVectorStore(
#                 index_name=self.index_name,
#                 embedding=self.embeddings
#             )

#         except Exception as e:
#             logger.error(f"Failed to initialize Pinecone: {e}")
#             raise

#     def add_documents(self, texts: list[str], metadatas: list[dict] = None):
#         """Add documents to vector store"""
#         try:
#             return self.vector_store.add_texts(texts, metadatas=metadatas)
#         except Exception as e:
#             logger.error(f"Failed to add documents: {e}")
#             return []

#     def similarity_search(self, query: str, k: int = 5):
#         """Search for similar documents"""
#         try:
#             return self.vector_store.similarity_search(query, k=k)
#         except Exception as e:
#             logger.error(f"Failed to search: {e}")
#             return []

# vector_store_service = VectorStoreService()


from pinecone import Pinecone, ServerlessSpec
from langchain_huggingface import HuggingFaceEndpointEmbeddings
from langchain_pinecone import PineconeVectorStore
from app.core.config import settings
import logging
import os

logger = logging.getLogger(__name__)


class VectorStoreService:
    _instance = None
    _vector_store = None
    _embeddings = None
    _initialized = False

    def __init__(self):
        pass

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        if not cls._initialized:
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        try:
            api_key = os.environ.get("PINECONE_API_KEY") or settings.PINECONE_API_KEY
            if not api_key:
                logger.warning("Pinecone API key not found, vector store disabled")
                return

            self.pc = Pinecone(api_key=api_key)
            self.index_name = "ai-agent-memory"

            hf_key = (
                os.environ.get("HUGGINGFACE_API_KEY") or settings.HUGGINGFACE_API_KEY
            )
            self._embeddings = HuggingFaceEndpointEmbeddings(
                model="sentence-transformers/all-MiniLM-L6-v2",
                huggingfacehub_api_token=hf_key,
            )

            if self.index_name not in self.pc.list_indexes().names():
                self.pc.create_index(
                    name=self.index_name,
                    dimension=384,
                    metric="cosine",
                    spec=ServerlessSpec(
                        cloud="aws", region=settings.PINECONE_ENVIRONMENT
                    ),
                )

            self._vector_store = PineconeVectorStore(
                index_name=self.index_name, embedding=self._embeddings
            )
            self._initialized = True
            logger.info("Pinecone vector store initialized successfully")

        except Exception as e:
            logger.error(f"Failed to initialize Pinecone: {e}")
            self._initialized = True  # Mark as initialized to avoid retry

    @classmethod
    def add_documents(cls, texts: list, metadatas: list = None):
        """Add documents to vector store"""
        try:
            instance = cls.get_instance()
            if instance._vector_store:
                return instance._vector_store.add_texts(
                    texts, metadatas=metadatas or []
                )
        except Exception as e:
            logger.error(f"Failed to add documents: {e}")
            return []

    @classmethod
    def similarity_search(cls, query: str, k: int = 5):
        """Search for similar documents"""
        try:
            instance = cls.get_instance()
            if instance._vector_store:
                return instance._vector_store.similarity_search(query, k=k)
        except Exception as e:
            logger.error(f"Failed to search: {e}")
            return []
