import asyncio
from typing import List, Dict, Any
from app.services.web_search import web_search_service_v2
from app.services.vector_store import VectorStoreService


async def search_web(query: str, num_results: int = 5) -> List[Dict[str, Any]]:
    """Search the web for information about a query. Returns list of results."""
    try:
        results = await web_search_service_v2.search_and_fetch(
            query=query, num_results=num_results, fetch_content=True
        )
        return results if results else []
    except Exception as e:
        logger.error(f"Search error: {str(e)}")
        return []


def retrieve_documents(query: str, k: int = 5) -> List[Dict[str, Any]]:
    """Retrieve relevant documents from the vector store. Returns list of documents."""
    try:
        docs = VectorStoreService.similarity_search(query, k=k)
        if not docs:
            return []

        return [
            {
                "title": doc.metadata.get("title", "Untitled"),
                "content": doc.page_content,
                "url": doc.metadata.get("url", ""),
            }
            for doc in docs
        ]
    except Exception as e:
        logger.error(f"Retrieval error: {str(e)}")
        return []


def get_source_url(title: str) -> str:
    """Get the source URL for a given document title."""
    try:
        docs = VectorStoreService.similarity_search(title, k=1)
        if docs and docs[0].metadata:
            return docs[0].metadata.get("url", "URL not found")
        return "Document not found"
    except Exception as e:
        return f"Error: {str(e)}"


import logging

logger = logging.getLogger(__name__)
