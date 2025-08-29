# app.py
import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

# -------------------------------
# Database connection (using secrets.toml if available)
# -------------------------------
db_url = st.secrets.get("database", {}).get(
    "url", "postgresql://postgres:TheK@host:5433/postgres"
)
engine = create_engine(db_url)

# -------------------------------
# Function to test DB query
# -------------------------------
def test_connection():
    try:
        with engine.connect() as conn:
            query = text("SELECT * FROM loancamdata LIMIT 5")
            result = conn.execute(query)
            df = pd.DataFrame(result.fetchall(), columns=result.keys())
            return df
    except SQLAlchemyError as e:
        st.error(f"Database error: {str(e)}")
        return pd.DataFrame()

# -------------------------------
# Streamlit Interface
# -------------------------------
st.title("🔗 Database Connectivity Test")

st.write("This small app tests if the database connection works correctly.")

if st.button("Test DB Connection"):
    df = test_connection()
    if not df.empty:
        st.success("✅ Successfully connected to database!")
        st.dataframe(df)
    else:
        st.error("❌ Could not retrieve data from the database.")
