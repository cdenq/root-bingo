# ----------------------------------
# IMPORTS
# ----------------------------------
import streamlit as st
from src.components import sidebar

# ----------------------------------
# FUNCTIONS
# ----------------------------------
def page_setup():
    st.set_page_config(
        page_title="Tofu's Root Bingo",
        layout="wide",
        initial_sidebar_state="expanded"
    )

# ----------------------------------
# MAIN
# ----------------------------------
def main():
    page_setup()

    sidebar.render()

if __name__ == "__main__":
    main()
