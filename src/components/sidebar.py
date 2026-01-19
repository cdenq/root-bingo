# ----------------------------------
# IMPORTS
# ----------------------------------
import streamlit as st
from src.pages import bingo, home, achievements

# ----------------------------------
# RENDER
# ----------------------------------
def render():
    pages = {
        "Home": home.render,
        "Bingo Sheet": bingo.render,
        "Bingo Wiki": achievements.render
    }

    st.sidebar.title("Navigation")
    selection = st.sidebar.radio("Go to", list(pages.keys()))

    pages[selection]()