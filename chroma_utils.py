import sys
import pysqlite3
sys.modules["sqlite3"] = pysqlite3
import os
from sentence_transformers import SentenceTransformer
import time

# Try to import ChromaDB, but make it optional
try:
    from chromadb import Client
    from chromadb.config import Settings
    CHROMADB_AVAILABLE = True
except ImportError:
    CHROMADB_AVAILABLE = False
    print("Warning: ChromaDB not available. Some features may be limited.")

# Initialize sentence transformer
try:
    embedder = SentenceTransformer("all-MiniLM-L6-v2")
    EMBEDDINGS_AVAILABLE = True
except Exception as e:
    EMBEDDINGS_AVAILABLE = False
    print(f"Warning: Sentence transformers not available: {e}")

def store_chapter_embeddings(book_id: str, chapters, content_type: str = "chapter", version: int = 1):
    """
    Store chapter (or other content) embeddings with versioning and type metadata.
    Falls back gracefully if ChromaDB is not available.
    """
    if not CHROMADB_AVAILABLE:
        print("ChromaDB not available - skipping embedding storage")
        return
    
    try:
        chroma_client = Client(Settings(persist_directory="./chroma_data"))
        collection = chroma_client.get_or_create_collection("bookbrain_chapters")
        
        if not EMBEDDINGS_AVAILABLE:
            print("Embeddings not available - skipping storage")
            return
            
        embeddings = embedder.encode(chapters).tolist()
        ids = [f"{book_id}_{content_type}_v{version}_ch_{i}" for i in range(len(chapters))]
        timestamp = int(time.time())
        metadatas = [{
            "book_id": book_id,
            "chapter": i,
            "type": content_type,
            "version": version,
            "timestamp": timestamp
        } for i in range(len(chapters))]
        collection.upsert(ids=ids, embeddings=embeddings, documents=chapters, metadatas=metadatas)
    except Exception as e:
        print(f"[ChromaDB] Error storing embeddings: {e}")

def store_content_version(book_id: str, content: str, content_type: str, chapter: int = 0, version: int = 1):
    """
    Store a single content version (summary, review, MCQs, or chapter) with metadata.
    Falls back gracefully if ChromaDB is not available.
    """
    if not CHROMADB_AVAILABLE:
        print("ChromaDB not available - skipping content storage")
        return
        
    try:
        chroma_client = Client(Settings(persist_directory="./chroma_data"))
        collection = chroma_client.get_or_create_collection("bookbrain_chapters")
        
        if not EMBEDDINGS_AVAILABLE:
            print("Embeddings not available - skipping storage")
            return
            
        embedding = embedder.encode([content]).tolist()[0]
        id = f"{book_id}_{content_type}_v{version}_ch_{chapter}"
        timestamp = int(time.time())
        metadata = {
            "book_id": book_id,
            "chapter": chapter,
            "type": content_type,
            "version": version,
            "timestamp": timestamp
        }
        collection.upsert(ids=[id], embeddings=[embedding], documents=[content], metadatas=[metadata])
    except Exception as e:
        print(f"[ChromaDB] Error storing content version: {e}")

def retrieve_content_versions(book_id: str, content_type: str, chapter: int = None):
    """
    Retrieve all versions of a given content type (and optionally chapter) for a book.
    Returns a list of dicts with content, version, and metadata.
    Falls back gracefully if ChromaDB is not available.
    """
    if not CHROMADB_AVAILABLE:
        print("ChromaDB not available - returning empty results")
        return []
        
    try:
        chroma_client = Client(Settings(persist_directory="./chroma_data"))
        collection = chroma_client.get_or_create_collection("bookbrain_chapters")
        
        # Query all documents for this book_id and type
        where = {"book_id": book_id, "type": content_type}
        if chapter is not None:
            where["chapter"] = chapter
        results = collection.get(where=where)
        out = []
        for doc, meta in zip(results["documents"], results["metadatas"]):
            out.append({
                "content": doc,
                "version": meta.get("version", 1),
                "metadata": meta
            })
        # Sort by version descending (latest first)
        out.sort(key=lambda x: x["version"], reverse=True)
        return out
    except Exception as e:
        print(f"[ChromaDB] Error retrieving content versions: {e}")
        return []

def semantic_search(query: str, top_k: int = 3):
    """
    Perform semantic search using embeddings.
    Falls back to simple text search if embeddings are not available.
    """
    if not CHROMADB_AVAILABLE or not EMBEDDINGS_AVAILABLE:
        print("ChromaDB or embeddings not available - using fallback search")
        return []
        
    try:
        chroma_client = Client(Settings(persist_directory="./chroma_data"))
        collection = chroma_client.get_or_create_collection("bookbrain_chapters")
        
        query_emb = embedder.encode([query]).tolist()[0]
        results = collection.query(query_embeddings=[query_emb], n_results=top_k)
        hits = []
        for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
            hits.append({"text": doc, "meta": meta})
        return hits
    except Exception as e:
        print(f"[ChromaDB] Error in semantic search: {e}")
        return [] 
