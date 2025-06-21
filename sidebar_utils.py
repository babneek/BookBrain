import streamlit as st

def show_sidebar():
    # This CSS hides the default Streamlit navigation section.
    st.markdown(
        """
        <style>
            [data-testid="stSidebarNav"] {display: none;}
        </style>
        """,
        unsafe_allow_html=True,
    )
    st.sidebar.page_link("streamlit_app.py", label="Home", icon="🏠")
    st.sidebar.page_link("pages/1_Summary.py", label="Summary", icon="📜")
    st.sidebar.page_link("pages/2_Review.py", label="Review", icon="🧠")
    st.sidebar.page_link("pages/3_MCQ.py", label="MCQ", icon="❓")
    st.sidebar.page_link("pages/4_QA.py", label="Q&A", icon="🗣️")