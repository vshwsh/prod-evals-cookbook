"""
Vector search tool for document retrieval.

Uses MongoDB to store documents and OpenAI embeddings for semantic search.
"""

from typing import Any

from langchain_core.tools import tool
from langchain_openai import OpenAIEmbeddings
from pymongo import MongoClient

from config import settings


def get_embeddings() -> OpenAIEmbeddings:
    """Get OpenAI embeddings client."""
    return OpenAIEmbeddings(
        model=settings.openai_embedding_model,
        openai_api_key=settings.openai_api_key,
    )


def get_mongodb_client() -> MongoClient:
    """Get MongoDB client."""
    return MongoClient(settings.mongodb_uri)


def cosine_similarity(a: list[float], b: list[float]) -> float:
    """Calculate cosine similarity between two vectors."""
    import numpy as np
    a_arr = np.array(a)
    b_arr = np.array(b)
    return float(np.dot(a_arr, b_arr) / (np.linalg.norm(a_arr) * np.linalg.norm(b_arr)))


def search_documents(query: str, top_k: int = 3) -> list[dict[str, Any]]:
    """
    Search documents using semantic similarity.
    
    Args:
        query: The search query
        top_k: Number of results to return
        
    Returns:
        List of matching documents with scores
    """
    # Generate query embedding
    embeddings = get_embeddings()
    query_embedding = embeddings.embed_query(query)
    
    # Get all documents from MongoDB
    client = get_mongodb_client()
    db = client[settings.mongodb_db]
    
    # Fetch all documents with embeddings
    # Note: In production, use MongoDB Atlas Vector Search for scalability
    documents = list(db.documents.find({}))
    
    if not documents:
        client.close()
        return []
    
    # Calculate similarity scores
    scored_docs = []
    for doc in documents:
        if "embedding" in doc:
            score = cosine_similarity(query_embedding, doc["embedding"])
            scored_docs.append({
                "filename": doc.get("filename", "unknown"),
                "category": doc.get("category", "unknown"),
                "content": doc.get("content", ""),
                "score": score,
            })
    
    # Sort by score and take top_k
    scored_docs.sort(key=lambda x: x["score"], reverse=True)
    results = scored_docs[:top_k]
    
    client.close()
    return results


@tool
def vector_search(query: str) -> str:
    """
    Search Acme Corp documents for information about policies, procedures, and guidelines.
    
    Use this tool for questions about:
    - HR policies (remote work, PTO, refunds)
    - Engineering practices (incidents, code review, on-call)
    - Product information (roadmap, pricing)
    
    Args:
        query: The question or topic to search for
        
    Returns:
        Relevant document excerpts with source information
    """
    results = search_documents(query, top_k=3)
    
    if not results:
        return "No relevant documents found."
    
    # Format results for the LLM (plain text, no markdown)
    formatted = []
    for i, doc in enumerate(results, 1):
        # Truncate content if too long
        content = doc["content"]
        # Strip markdown formatting from content
        content = content.replace("**", "").replace("*", "").replace("#", "").replace("`", "")
        if len(content) > 2000:
            content = content[:2000] + "\n\n[Content truncated...]"
        
        formatted.append(
            f"[Source {i}: {doc['filename']}] (category: {doc['category']}, relevance: {doc['score']:.2f})\n\n"
            f"{content}"
        )
    
    return "\n\n" + ("=" * 40) + "\n\n".join(formatted)


# For direct testing
if __name__ == "__main__":
    # Test the search
    test_queries = [
        "What is the remote work policy?",
        "How do I handle a production incident?",
        "What are our pricing tiers?",
    ]
    
    for query in test_queries:
        print(f"\n{'='*60}")
        print(f"Query: {query}")
        print("="*60)
        result = vector_search.invoke({"query": query})
        print(result[:500] + "..." if len(result) > 500 else result)
