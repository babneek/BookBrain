from chroma_utils import store_chapter_embeddings, semantic_search, retrieve_content_versions
from llm_utils import generate_summary, generate_review, generate_mcqs, client, MODEL_NAME
from epub_utils import extract_chapters_from_epub
import os
from dotenv import load_dotenv

load_dotenv()

def chunk_text(text, chunk_size=12000):
    # Split text into chunks of max chunk_size characters
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size) if text[i:i+chunk_size].strip()]

# --- Q&A PIPELINE ---
def answer_question(query: str, model: str = None) -> dict:
    """
    Answers a user question using semantic search for context and OpenRouter LLM.
    Returns a dict with 'answer' and 'context_chunks'.
    """
    try:
        import streamlit as st
        # Use the selected chapter from session state, chunk it, and run semantic search over chunks
        text = None
        if hasattr(st.session_state, 'extracted_text'):
            text = st.session_state["extracted_text"]
        if not text:
            return {"answer": "[Error] No chapter text found for Q/A.", "context_chunks": []}
        chunks = chunk_text(text, chunk_size=12000)
        # Use a simple embedding search over chunks
        from sentence_transformers import SentenceTransformer
        embedder = SentenceTransformer("all-MiniLM-L6-v2")
        query_emb = embedder.encode([query]).tolist()[0]
        # Compute similarity for each chunk
        import numpy as np
        chunk_embs = embedder.encode(chunks)
        sims = [np.dot(query_emb, chunk_emb) for chunk_emb in chunk_embs]
        # Get top 2 most relevant chunks
        top_indices = np.argsort(sims)[-2:][::-1]
        context_chunks = [chunks[i] for i in top_indices]
        # Hard cap on context length
        context = "\n\n".join(context_chunks)
        if len(context) > 24000:
            context = context[:24000]
        prompt = f"Use the following context to answer the question in detail.\n\nContext:\n{context}\n\nQuestion: {query}\nAnswer:"
        response = client.chat.completions.create(
            model=model or MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=600,
        )
        answer = response.choices[0].message.content.strip()
        # Fallback: if answer says 'no information' or 'not found', show most relevant passage
        if any(x in answer.lower() for x in ["no information", "not found", "no details", "no context"]):
            answer += "\n\nMost relevant passage:\n" + (context_chunks[0] if context_chunks else "[No context found]")
        return {"answer": answer, "context_chunks": context_chunks}
    except Exception as e:
        return {"answer": f"[Error] Failed to answer question: {e}", "context_chunks": []}

# --- FEEDBACK STORE (in-memory for demo) ---
feedback_store = []
def store_feedback(question, answer, correct, user_feedback):
    """
    Stores user feedback on Q&A results (in-memory for demo purposes).
    """
    feedback_store.append({
        "question": question,
        "answer": answer,
        "correct": correct,
        "user_feedback": user_feedback
    })

# --- RL-INSPIRED SEARCH ---
def rl_semantic_search(query: str, top_k: int = 3):
    """
    RL-inspired semantic search: boosts content with positive feedback for similar questions.
    Returns top_k results, ranked by embedding similarity and feedback reward.
    """
    try:
        hits = semantic_search(query, top_k=10)  # Get more candidates
        # Assign a reward score based on feedback_store
        def feedback_reward(hit_text):
            reward = 0
            for fb in feedback_store:
                if fb["user_feedback"] == "Yes" and fb["answer"] in hit_text:
                    reward += 1
                elif fb["user_feedback"] == "No" and fb["answer"] in hit_text:
                    reward -= 1
            return reward
        # Sort by reward, then by original order (embedding similarity)
        hits.sort(key=lambda h: (feedback_reward(h["text"]),), reverse=True)
        return hits[:top_k]
    except Exception as e:
        print(f"[RL Search] Error: {e}")
        return []

# --- PIPELINE ORCHESTRATION EXAMPLE ---
def process_chapter(text: str, model: str = None):
    """
    Runs the full pipeline for a chapter: summary, review, MCQs.
    Returns a dict with all outputs.
    """
    summary = generate_summary(text)
    review = generate_review(text)
    mcqs = generate_mcqs(text, 5)
    return {
        "summary": summary,
        "review": review,
        "mcqs": mcqs
    } 