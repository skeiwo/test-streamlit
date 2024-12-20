import pandas as pd
from sqlalchemy import create_engine
import streamlit as st

db_url = "postgresql://postgres:postgres@localhost:5432/bezrealitky"
engine = create_engine(db_url)

query = "SELECT price_czk, disposition, size_m2, street, district, href FROM etl_rent WHERE scrape_timestamp = (SELECT MAX(scrape_timestamp) FROM etl_rent)"
df = pd.read_sql(query, engine)

# Streamlit App
st.title("Flats in Prague for rent")

# Price Filter
price_filter = st.sidebar.slider(
    "Select Price Range (CZK):", min_value=10000, max_value=40000, value=(10000, 40000)
)

# Disposition Single Select
disposition_filter = st.sidebar.selectbox(
    "Select Disposition:", options=["All"] + list(df["disposition"].unique())
)

# Apply filters
filtered_df = df[
    (df["price_czk"] >= price_filter[0]) &
    (df["price_czk"] <= price_filter[1]) &
    ((df["disposition"] == disposition_filter) if disposition_filter != "All" else True)
]

# Display Filtered DataFrame
st.dataframe(filtered_df)