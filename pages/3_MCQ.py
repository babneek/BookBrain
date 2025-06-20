import streamlit as st
from llm_utils import generate_mcqs
from sidebar_utils import show_sidebar
import re

def try_generate_mcqs(text, n=5, max_retries=3):
    for attempt in range(max_retries):
        mcq_text = generate_mcqs(text, n)
        parsed = parse_mcqs(mcq_text)
        if parsed:
            return mcq_text, parsed
    return mcq_text, parsed  # Return last attempt (even if empty)

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

def parse_mcqs(mcq_text):
    try:
        questions = re.split(r'\n\d+\. ', mcq_text)
        questions = [q.strip() for q in questions if q.strip()]
        parsed = []
        for q in questions:
            q_lines = q.split('\n')
            if len(q_lines) < 3:
                continue
            question = q_lines[0]
            options = [line for line in q_lines[1:] if re.match(r'^[A-D]\.', line.strip())]
            answer_line = next((line for line in q_lines if 'Correct answer' in line or 'Answer:' in line), None)
            explanation = next((line for line in q_lines if 'Explanation' in line), None)
            if not options or not answer_line:
                continue
            correct_option = re.search(r'([A-D])', answer_line)
            correct = correct_option.group(1) if correct_option else None
            parsed.append({
                'question': question,
                'options': options,
                'answer': correct,
                'answer_line': answer_line,
                'explanation': explanation
            })
        return parsed
    except Exception as e:
        st.error(f"Error parsing MCQs: {e}")
        return []

def interactive_mcq_quiz(parsed_mcqs):
    if 'mcq_score' not in st.session_state:
        st.session_state['mcq_score'] = 0
    if 'mcq_index' not in st.session_state:
        st.session_state['mcq_index'] = 0
    if 'mcq_done' not in st.session_state:
        st.session_state['mcq_done'] = False
    if 'mcq_show_feedback' not in st.session_state:
        st.session_state['mcq_show_feedback'] = False
    if 'mcq_last_correct' not in st.session_state:
        st.session_state['mcq_last_correct'] = False
    total = len(parsed_mcqs)
    idx = st.session_state['mcq_index']
    score = st.session_state['mcq_score']
    if st.session_state['mcq_done']:
        # Colorful result message based on score
        if score == total:
            msg = "🎉 <span style='color:#219653; font-weight:bold; font-size:1.3em;'>Excellent! You got a perfect score!</span>"
            bg = "#e6f9ed"
        elif score >= total * 0.7:
            msg = "😊 <span style='color:#2d9cdb; font-weight:bold; font-size:1.2em;'>Great job! You scored high!</span>"
            bg = "#eaf6ff"
        elif score >= total * 0.4:
            msg = "👍 <span style='color:#f2c94c; font-weight:bold; font-size:1.1em;'>Not bad! Keep practicing.</span>"
            bg = "#fffbe6"
        elif score == 1:
            msg = "😅 <span style='color:#eb5757; font-weight:bold; font-size:1.1em;'>Better luck next time!</span>"
            bg = "#ffeaea"
        else:
            msg = "😢 <span style='color:#eb5757; font-weight:bold; font-size:1.1em;'>Don't give up! Try again.</span>"
            bg = "#ffeaea"
        st.markdown(f"""
        <div style='background:{bg}; border-radius:12px; padding:1.5em; margin-bottom:1.2em; text-align:center;'>
            <div style='font-size:1.3em; font-weight:bold; color:#2d6a4f; margin-bottom:0.5em;'>Quiz Complete! Your Score: {score} / {total}</div>
            {msg}
        </div>
        """, unsafe_allow_html=True)
        # Download, Regenerate, Edit buttons below result
        col1, col2, col3 = st.columns([1,1,2])
        with col1:
            if st.button("✏️ Edit", key="edit_btn_done"):
                st.session_state["edit_mode"] = True
        with col2:
            if st.button("🔄 Regenerate MCQs", key="regen_btn_done"):
                with st.spinner("Regenerating MCQs..."):
                    text = st.session_state["extracted_text"]
                    mcq_text, parsed_mcqs = try_generate_mcqs(text, 5)
                    st.session_state["mcqs"] = mcq_text
                    st.session_state["parsed_mcqs"] = parsed_mcqs
                    st.rerun()
        with col3:
            st.download_button("⬇️ Download MCQs", st.session_state["mcqs"], file_name="mcqs.txt")
        if st.button("🔁 Retry Quiz"):
            for k in list(st.session_state.keys()):
                if k.startswith("mcq_") or k in ['mcq_score','mcq_index','mcq_done','mcq_show_feedback','mcq_last_correct']:
                    del st.session_state[k]
            st.rerun()
        return
    q = parsed_mcqs[idx]
    st.markdown(f"<div style='background:#f8f9fa; border-radius:12px; box-shadow:0 1px 6px #0001; padding:1.2em; margin-bottom:1.2em;'><b style='font-size:1.1em;'>Q{idx+1}. {q['question']}</b>", unsafe_allow_html=True)
    user_ans = st.radio("Select an option:", q['options'], key=f"mcq_{idx}")
    if not st.session_state['mcq_show_feedback']:
        if st.button("Submit", key=f"mcq_btn_{idx}"):
            if user_ans.startswith(q['answer']):
                st.session_state['mcq_last_correct'] = True
                st.session_state['mcq_score'] += 1
            else:
                st.session_state['mcq_last_correct'] = False
            st.session_state['mcq_show_feedback'] = True
            st.rerun()
    else:
        if st.session_state['mcq_last_correct']:
            st.success("Correct!")
        else:
            st.error(f"Incorrect. {q['answer_line']}")
        if q['explanation']:
            st.info(q['explanation'])
        if idx + 1 < total:
            if st.button("Next", key=f"mcq_next_{idx}"):
                st.session_state['mcq_index'] += 1
                st.session_state['mcq_show_feedback'] = False
                st.rerun()
        else:
            if st.button("Finish Quiz", key=f"mcq_finish_{idx}"):
                st.session_state['mcq_done'] = True
                st.session_state['mcq_show_feedback'] = False
                st.rerun()
    st.markdown(f"<div style='margin-top:1em; color:#888;'>Question {idx+1} of {total} | Score: {score}</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

def main():
    show_sidebar(current_page="MCQ")
    show_logo_and_branding()
    if "extracted_text" not in st.session_state:
        st.warning("No text found. Please upload a file or process a Wiki URL on the Home page.")
        if st.button("⬅️ Back to Home", key="back_home_btn"):
            st.switch_page("streamlit_app.py")
        return
    # Always use the currently selected chapter
    text = st.session_state["extracted_text"]
    if "mcqs" not in st.session_state:
        with st.spinner("Generating MCQs..."):
            try:
                mcq_text, parsed_mcqs = try_generate_mcqs(text, 5)
                st.session_state["mcqs"] = mcq_text
                st.session_state["parsed_mcqs"] = parsed_mcqs
            except Exception as e:
                st.error(f"Failed to generate MCQs: {e}")
                return
    if "edit_mode" not in st.session_state:
        st.session_state["edit_mode"] = False
    st.markdown("""
    <div style='background: #fff; border-radius: 16px; box-shadow: 0 2px 12px #0001; padding: 2em 2em 1em 2em; margin-bottom: 2em;'>
        <h2 style='margin-top:0;'>📝 MCQ Quiz</h2>
    """, unsafe_allow_html=True)
    if not st.session_state["edit_mode"]:
        col1, col2, col3 = st.columns([1,1,2])
        with col1:
            if st.button("✏️ Edit", key="edit_btn"):
                st.session_state["edit_mode"] = True
        with col2:
            if st.button("🔄 Regenerate MCQs", key="regen_btn"):
                with st.spinner("Regenerating MCQs..."):
                    # Always use the currently selected chapter
                    text = st.session_state["extracted_text"]
                    mcq_text, parsed_mcqs = try_generate_mcqs(text, 5)
                    st.session_state["mcqs"] = mcq_text
                    st.session_state["parsed_mcqs"] = parsed_mcqs
                    st.rerun()
        with col3:
            st.download_button("⬇️ Download MCQs", st.session_state["mcqs"], file_name="mcqs.txt")
        st.markdown("<br>", unsafe_allow_html=True)
        parsed_mcqs = st.session_state.get("parsed_mcqs")
        if not parsed_mcqs:
            st.error("No valid MCQs found after several attempts. Please try editing or regenerating the MCQs.")
        else:
            interactive_mcq_quiz(parsed_mcqs)
    else:
        new_mcqs = st.text_area("Edit MCQs", value=st.session_state["mcqs"], height=300, key="mcqs_edit")
        colA, colB = st.columns([1,1])
        with colA:
            if st.button("💾 Save", key="save_btn"):
                st.session_state["mcqs"] = new_mcqs
                st.session_state["edit_mode"] = False
                st.success("MCQs updated!")
        with colB:
            if st.button("❌ Cancel", key="cancel_btn"):
                st.session_state["edit_mode"] = False
        st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("<center style='color:#888;'>Made with ❤️ by BookBrain</center>", unsafe_allow_html=True)

if __name__ == "__main__":
    main() 