import streamlit as st
import pandas as pd
from sqlalchemy import create_engine



st.title("Hello, world!")
st.header("This is a header", divider=True)
st.markdown("This is a markdown text.")

col1, col2 = st.columns(2)

with col1:
    x = st.slider("Select a value", 1, 10)

with col2:
    st.write(f"You selected {x}")