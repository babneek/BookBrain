import streamlit as st
from llm_utils import generate_mcqs
from sidebar_utils import show_sidebar
import re

def try_generate_mcqs(text, n=5, max_retries=2):
    """Attempt to generate and parse MCQs, retrying on failure."""
    for _ in range(max_retries):
        mcq_text = generate_mcqs(text, n)
        if mcq_text and not mcq_text.startswith("[Error]"):
            parsed = parse_mcqs(mcq_text)
            if parsed:
                return mcq_text, parsed
    return "Could not generate valid MCQs.", []

def show_logo_and_branding():
    """Displays the app logo and branding in the main content area."""
    st.markdown(
        """
        <div style='display: flex; align-items: center; gap: 1em; margin-bottom: 1em;'>
            <img src='https://emojicdn.elk.sh/📚' width='48' style='vertical-align: middle;'>
            <span style='font-size: 2rem; font-weight: bold; color: #3B3B3B;'>BookBrain</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

def parse_mcqs(mcq_text):
    """
    Parses raw text from an LLM into a structured list of MCQ dictionaries
    using a more robust regex to handle formatting variations.
    """
    mcq_pattern = re.compile(
        r'(\d+)\.\s*(.*?)\n\s*'
        r'(A\.\s*.*?)\n\s*'
        r'(B\.\s*.*?)\n\s*'
        r'(C\.\s*.*?)\n\s*'
        r'(D\.\s*.*?)\n\s*'
        r'Correct answer:\s*([A-D])\n'
        r'(?:Explanation:\s*(.*?))?',
        re.DOTALL | re.MULTILINE
    )
    
    parsed = []
    matches = mcq_pattern.finditer(mcq_text)
    
    for match in matches:
        question = match.group(2).strip()
        options = [
            match.group(3).strip(),
            match.group(4).strip(),
            match.group(5).strip(),
            match.group(6).strip()
        ]
        answer = match.group(7).strip()
        explanation = match.group(8).strip() if match.group(8) else "No explanation provided."
        
        parsed.append({
            'question': question,
            'options': options,
            'answer': answer,
            'explanation': explanation
        })
    return parsed

def interactive_mcq_quiz(parsed_mcqs):
    """Manages the interactive MCQ quiz state and UI."""
    st.session_state.setdefault('mcq_score', 0)
    st.session_state.setdefault('mcq_index', 0)
    st.session_state.setdefault('mcq_done', False)
    st.session_state.setdefault('mcq_show_feedback', False)
    st.session_state.setdefault('mcq_last_correct', False)

    idx = st.session_state.mcq_index
    total = len(parsed_mcqs)

    if st.session_state.mcq_done:
        score = st.session_state.mcq_score
        st.success(f"🎉 Quiz Complete! Your final score is: {score}/{total}")
        if st.button("🔁 Retry Quiz", key="retry_quiz"):
            for k in list(st.session_state.keys()):
                if isinstance(k, str) and k.startswith('mcq_'):
                    del st.session_state[k]
            st.rerun()
        return

    q = parsed_mcqs[idx]
    st.markdown(f"**Question {idx + 1}/{total}:**")
    st.markdown(f"*{q['question']}*")

    user_ans = st.radio("Select your answer:", q['options'], key=f"mcq_radio_{idx}")

    if st.session_state.mcq_show_feedback:
        if st.session_state.mcq_last_correct:
            st.success("Correct!")
        else:
            st.error(f"Incorrect. The correct answer was **{q['answer']}**.")
        st.info(f"**Explanation:** {q['explanation']}")

        if idx + 1 < total:
            if st.button("Next Question", key=f"next_q_btn_{idx}"):
                st.session_state.mcq_index += 1
                st.session_state.mcq_show_feedback = False
                st.rerun()
        else:
            if st.button("Finish Quiz", key=f"finish_quiz_btn"):
                st.session_state.mcq_done = True
                st.session_state.mcq_show_feedback = False
                st.rerun()
    else:
        if st.button("Submit", key=f"submit_btn_{idx}"):
            if user_ans is None:
                st.warning("⚠️ Please select an answer before submitting.")
            else:
                selected_letter = user_ans.split('.')[0].strip().upper()
                correct_letter = q['answer'].strip().upper()

                if selected_letter == correct_letter:
                    st.session_state.mcq_score += 1
                    st.session_state.mcq_last_correct = True
                else:
                    st.session_state.mcq_last_correct = False

                st.session_state.mcq_show_feedback = True
                st.rerun()
    
    st.progress((idx + 1) / total)

def main():
    """Main function to render the MCQ page."""
    show_sidebar()
    show_logo_and_branding()

    if "extracted_text" not in st.session_state:
        st.warning("Please upload a file or enter a URL on the Home page first.")
        if st.button("⬅️ Back to Home", key="mcq_back_home"):
            st.switch_page("streamlit_app.py")
        return

    text = st.session_state.extracted_text
    
    if "parsed_mcqs" not in st.session_state:
        with st.spinner("Generating MCQs for you..."):
            mcq_text, parsed_mcqs = try_generate_mcqs(text)
            st.session_state.mcqs = mcq_text
            st.session_state.parsed_mcqs = parsed_mcqs
    
    parsed_mcqs = st.session_state.get("parsed_mcqs", [])

    st.markdown("---")
    if not parsed_mcqs:
        st.error("Failed to generate or parse MCQs from the text. Please try again.")
    else:
        st.header("📝 Take a Quiz!")
        interactive_mcq_quiz(parsed_mcqs)

    st.markdown("---")
    st.header("Manage MCQs")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Regenerate MCQs", key="regenerate_mcqs_btn"):
            with st.spinner("Getting a fresh set of questions..."):
                mcq_text, parsed_mcqs = try_generate_mcqs(text)
                st.session_state.mcqs = mcq_text
                st.session_state.parsed_mcqs = parsed_mcqs
                for k in list(st.session_state.keys()):
                    if isinstance(k, str) and k.startswith('mcq_'):
                        del st.session_state[k]
                st.rerun()
    with col2:
        st.download_button(
            label="⬇️ Download MCQs",
            data=st.session_state.get("mcqs", "No MCQs available."),
            file_name="mcqs.txt",
            key="download_mcqs_btn"
        )

if __name__ == "__main__":
    main() 


