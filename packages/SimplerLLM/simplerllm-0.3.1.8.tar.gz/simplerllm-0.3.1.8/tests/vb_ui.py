import streamlit as st
import numpy as np
import os
from SimplerLLM.vectors.vector_storage import VectorDatabase, SerializationFormat
import pandas as pd
import asyncio

async def load_database(file_path):
    db = VectorDatabase("temp_db")
    file_extension = os.path.splitext(file_path)[1]
    
    if file_extension == '.svdb':
        serialization_format = SerializationFormat.BINARY
    elif file_extension == '.json':
        serialization_format = SerializationFormat.JSON
    else:
        st.error(f"Unsupported file format: {file_extension}")
        return None

    await db.load_from_disk(file_path, serialization_format)
    return db

def display_database_stats(db):
    st.subheader("Database Statistics")
    st.write(f"Number of records: {len(db.metadata)}")
    st.write(f"Vector dimension: {db.vectors.shape[1] if len(db.vectors) > 0 else 0}")
    st.write(f"Use semantic connections: {db.use_semantic_connections}")
    st.write(f"Index: {db.next_id}")

def display_database_content(db):
    st.subheader("Database Content")
    
    if not db.metadata:
        st.write("The database is empty.")
        return

    # Create a DataFrame from the metadata
    df = pd.DataFrame(db.metadata)
    
    # Drop the 'embedding' column if it exists
    if 'embedding' in df.columns:
        df = df.drop(columns=['embedding'])
    
    # Display the DataFrame
    st.dataframe(df)

async def process_file(file_path):
    db = await load_database(file_path)
    if db is not None:
        display_database_stats(db)
        display_database_content(db)

def main():
    st.title("Vector Database Viewer")

    uploaded_file = st.file_uploader("Choose a database file", type=['svdb', 'json'])
    
    if uploaded_file is not None:
        with st.spinner("Loading database..."):
            # Save the uploaded file temporarily
            temp_file_path = f"temp_{uploaded_file.name}"
            with open(temp_file_path, "wb") as temp_file:
                temp_file.write(uploaded_file.getbuffer())
            
            # Use asyncio to run the asynchronous function
            asyncio.run(process_file(temp_file_path))
            
            # Remove the temporary file
            os.remove(temp_file_path)

if __name__ == "__main__":
    main()