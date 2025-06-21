import streamlit as st
from pipeline import answer_question, store_feedback
from sidebar_utils import show_sidebar

def show_logo_and_branding():
    st.markdown(
        """
        <div style='display: flex; align-items: center; gap: 1em; margin-bottom: 1em;'>
            <img src='https://emojicdn.elk.sh/📚' width='48' style='vertical-align: middle;'>
            <span style='font-size: 2rem; font-weight: bold; color: #3B3B3B;'>BookBrain</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

def main():
    show_sidebar()
    show_logo_and_branding()
    if "extracted_text" not in st.session_state:
        st.warning("No text found. Please upload a file or process a Wiki URL on the Home page.")
        if st.button("⬅️ Back to Home", key="back_home_btn"):
            st.switch_page("streamlit_app.py")
        return
    st.markdown("""
    <div style='background: #fff; border-radius: 16px; box-shadow: 0 2px 12px #0001; padding: 2em 2em 1em 2em; margin-bottom: 2em;'>
        <h2 style='margin-top:0;'>❓ Q/A</h2>
    """, unsafe_allow_html=True)
    user_q = st.text_input("Ask a question about the uploaded or extracted content:", key="qa_input", placeholder="Type your question here...", help="Ask anything about the book or content.")
    if user_q and st.button("Get Answer", key="qa_btn"):
        with st.spinner("Answering..."):
            try:
                result = answer_question(user_q)
                answer = result["answer"]
                context_chunks = result["context_chunks"]
                if answer.startswith("[Error]"):
                    st.error(answer)
                else:
                    st.session_state["last_answer"] = answer
                    st.session_state["last_question"] = user_q
                    st.session_state["last_context_chunks"] = context_chunks
            except Exception as e:
                st.error(f"Failed to get answer. Please check your OpenAI API key and ChromaDB setup. Error: {e}")
                return
    if "last_answer" in st.session_state and "last_question" in st.session_state:
        st.markdown(f"<div style='background:#f8f9fa; border-radius:12px; box-shadow:0 1px 6px #0001; padding:1.2em; margin-bottom:1.2em;'><b style='font-size:1.1em;'>Q: {st.session_state['last_question']}</b><br><br><span style='font-size:1.1em;'>A: {st.session_state['last_answer']}</span></div>", unsafe_allow_html=True)
        # Show retrieved context for transparency
        if "last_context_chunks" in st.session_state and st.session_state["last_context_chunks"]:
            with st.expander("Show retrieved context", expanded=False):
                for i, chunk in enumerate(st.session_state["last_context_chunks"]):
                    st.markdown(f"**Context Chunk {i+1}:**\n<pre style='white-space:pre-wrap'>{chunk}</pre>", unsafe_allow_html=True)
        st.markdown("<div style='margin-bottom:1em;'></div>", unsafe_allow_html=True)
        col1, col2 = st.columns([1,1])
        with col1:
            if st.button("👍 Helpful", key="fb_yes"):
                store_feedback(st.session_state["last_question"], st.session_state["last_answer"], True, "Yes")
                st.success("Thank you for your feedback!")
                del st.session_state["last_answer"]
                del st.session_state["last_question"]
                if "last_context_chunks" in st.session_state:
                    del st.session_state["last_context_chunks"]
        with col2:
            if st.button("👎 Not Helpful", key="fb_no"):
                store_feedback(st.session_state["last_question"], st.session_state["last_answer"], False, "No")
                st.success("Thank you for your feedback!")
                del st.session_state["last_answer"]
                del st.session_state["last_question"]
                if "last_context_chunks" in st.session_state:
                    del st.session_state["last_context_chunks"]
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("<center style='color:#888;'>Made with ❤️ by BookBrain</center>", unsafe_allow_html=True)

if __name__ == "__main__":
    main() 