# ----------------------------------
# IMPORTS
# ----------------------------------
import streamlit as st
from config.settings import TOFU_IMAGE

# ----------------------------------
# RENDER MAIN
# ----------------------------------
def render():
    st.image(str(TOFU_IMAGE), width=150)
    st.title("Tofu's Root Bingo Generator")
    st.markdown("---")
    st.write("Bingo generator for Root. Navigate via sidebar.")
