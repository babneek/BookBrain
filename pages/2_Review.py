import streamlit as st
from llm_utils import generate_review
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
    show_sidebar(current_page="Review")
    show_logo_and_branding()
    if "extracted_text" not in st.session_state:
        st.warning("No text found. Please upload a file or process a Wiki URL on the Home page.")
        if st.button("⬅️ Back to Home", key="back_home_btn"):
            st.switch_page("streamlit_app.py")
        return
    text = st.session_state["extracted_text"]
    if "review" not in st.session_state:
        st.session_state["review"] = generate_review(text)
    if "edit_mode" not in st.session_state:
        st.session_state["edit_mode"] = False
    st.markdown("""
    <div style='background: #fff; border-radius: 16px; box-shadow: 0 2px 12px #0001; padding: 2em 2em 1em 2em; margin-bottom: 2em;'>
        <h2 style='margin-top:0;'>🧠 Review</h2>
    """, unsafe_allow_html=True)
    if not st.session_state["edit_mode"]:
        st.markdown(f"<div style='font-size:1.2em; line-height:1.7; margin-bottom:1.5em;'>{st.session_state['review'].replace(chr(10),'<br>')}</div>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1,1,2])
        with col1:
            if st.button("✏️ Edit", key="edit_btn"):
                st.session_state["edit_mode"] = True
        with col2:
            if st.button("🔄 Regenerate Review", key="regen_btn"):
                with st.spinner("Regenerating review..."):
                    st.session_state["review"] = generate_review(text)
                    st.rerun()
        with col3:
            st.download_button("⬇️ Download Review", st.session_state["review"], file_name="review.txt")
    else:
        new_review = st.text_area("Edit Review", value=st.session_state["review"], height=300, key="review_edit")
        colA, colB = st.columns([1,1])
        with colA:
            if st.button("💾 Save", key="save_btn"):
                st.session_state["review"] = new_review
                st.session_state["edit_mode"] = False
                st.success("Review updated!")
        with colB:
            if st.button("❌ Cancel", key="cancel_btn"):
                st.session_state["edit_mode"] = False
        st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("<center style='color:#888;'>Made with ❤️ by BookBrain</center>", unsafe_allow_html=True)

if __name__ == "__main__":
    main() 