import streamlit as st

def show_sidebar(current_page="Home"):
    # Hide default Streamlit navigation
    st.markdown(
        '''
        <style>
        [data-testid="stSidebarNav"] {display: none !important;}
        </style>
        ''',
        unsafe_allow_html=True
    )
    st.sidebar.markdown(
        """
        <div style='text-align:center; margin-bottom:2em;'>
            <img src='https://emojicdn.elk.sh/📘' width='60' style='border-radius:12px; margin-bottom:0.5em;'>
            <div style='font-size:1.5em; font-weight:bold; color:#2d3a4a;'>BookBrain</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    nav_items = [
        ("Home", "streamlit_app.py"),
        ("Summary", "pages/1_Summary.py"),
        ("Review", "pages/2_Review.py"),
        ("MCQ", "pages/3_MCQ.py"),
        ("QA", "pages/4_QA.py"),
    ]
    for name, page in nav_items:
        selected = (name == current_page)
        btn = st.sidebar.button(
            name,
            key=f"sidebar_{name}",
            help=f"Go to {name}",
        )
        if btn and not selected:
            st.switch_page(page)
        st.sidebar.markdown(
            f"""
            <style>
            [data-testid="stSidebar"] .element-container:nth-child({nav_items.index((name, page))+2}) button {{
                background: {'#4f8cff' if selected else 'transparent'} !important;
                color: {'#fff' if selected else '#2d3a4a'} !important;
                font-weight: {'bold' if selected else 'normal'};
                border-radius: 8px;
                margin-bottom: 0.7em;
                font-size: 1.1em;
                padding: 0.7em 1.2em;
            }}
            </style>
            """,
            unsafe_allow_html=True,
        )
    # Add custom CSS for sidebar and main content
    st.markdown(
        """
        <style>
        .block-container { background: #f7faff; border-radius: 18px; padding: 2em 2em 1em 2em; }
        .stSidebar { background: linear-gradient(180deg, #e3f0ff 0%, #f7faff 100%); }
        .stApp { background: #f7faff; }
        </style>
        """,
        unsafe_allow_html=True,
    ) 