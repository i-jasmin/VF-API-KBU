import streamlit as st
import pandas as pd
import requests
import os
from dotenv import load_dotenv
from io import BytesIO

# Configure environment
load_dotenv()
st.set_page_config(page_title="Excel/CSV to Voiceflow", layout="wide")

# Get API key from .env
VOICEFLOW_API_KEY = os.getenv('VOICEFLOW_API_KEY')
UPLOAD_URL = 'https://api.voiceflow.com/v1/knowledge-base/docs/upload/table'

def main():
    st.title("Excel/CSV to Voiceflow Knowledge Base Uploader")
    
    # File upload section
    uploaded_file = st.file_uploader("Upload File", type=["xlsx", "xls", "csv"])
    
    if uploaded_file:
        try:
            # Determine file type
            file_extension = uploaded_file.name.split('.')[-1].lower()
            
            # Read file based on type
            if file_extension == 'csv':
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
            
            columns = df.columns.tolist()
            
            # Table name input
            table_name = st.text_input(
                "Table Name",
                value=uploaded_file.name.split('.')[0],
                help="Name for this table in Voiceflow Knowledge Base"
            )
            
            # Field selection
            st.subheader("Field Configuration")
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Searchable Fields**")
                searchable_fields = st.multiselect(
                    "Select fields to be searchable",
                    columns,
                    key="searchable"
                )
                
            with col2:
                st.markdown("**Metadata Fields**")
                metadata_fields = st.multiselect(
                    "Select metadata fields",
                    columns,
                    key="metadata"
                )
            
            # Data transformation and upload
            if st.button("Preview & Upload"):
                if not table_name:
                    st.error("Please enter a table name")
                    st.stop()
                
                # Convert dataframe to items
                items = []
                for _, row in df.iterrows():
                    item = {col: str(row[col]) for col in columns}
                    items.append(item)
                
                # Create payload structure
                payload = {
                    "data": {
                        "schema": {
                            "searchableFields": searchable_fields,
                            "metadataFields": metadata_fields
                        },
                        "name": table_name,
                        "items": items
                    }
                }
                
                # Show preview
                st.subheader("Data Preview")
                st.write(f"Total rows: {len(items)}")
                st.dataframe(df.head(3))
                
                # Upload to Voiceflow
                headers = {
                    "Authorization": VOICEFLOW_API_KEY,
                    "Content-Type": "application/json",
                    "accept": "application/json"
                }
                
                response = requests.post(
                    f"{UPLOAD_URL}?overwrite=true",
                    headers=headers,
                    json=payload
                )
                
                if response.status_code == 200:
                    st.success("Successfully uploaded to Voiceflow Knowledge Base!")
                    st.balloons()
                    st.json(response.json())
                else:
                    st.error(f"Upload failed: {response.text}")
        
        except Exception as e:
            st.error(f"Error processing file: {str(e)}")

if __name__ == "__main__":
    if not VOICEFLOW_API_KEY:
        st.error("Missing VOICEFLOW_API_KEY in .env file")
    else:
        main()