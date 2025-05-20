import streamlit as st
import pandas as pd
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Streamlit page
st.set_page_config(page_title="Data Upload to Voiceflow", layout="wide")

# Get Voiceflow API key from environment
VOICEFLOW_API_KEY = os.getenv('VOICEFLOW_API_KEY')
UPLOAD_URL = 'https://api.voiceflow.com/v1/knowledge-base/docs/upload/table'

def main():
    st.title("📤 Data Upload to Voiceflow Knowledge Base")
    
    # File upload section
    uploaded_file = st.file_uploader("Choose a file", type=["xlsx", "xls", "csv"])
    
    if uploaded_file:
        try:
            # Read file based on type
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
            
            # Get columns and setup UI
            columns = df.columns.tolist()
            
            # Table name input
            table_name = st.text_input(
                "Table Name",
                value=uploaded_file.name.split('.')[0],
                help="Name for this table in Voiceflow Knowledge Base"
            )
            
            # Field selection columns
            st.subheader("⚙️ Field Configuration")
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**🔍 Searchable Fields**")
                searchable_fields = st.multiselect(
                    "Select fields used for search",
                    columns,
                    key="searchable"
                )
                
            with col2:
                st.markdown("**🏷️ Metadata Fields**")
                metadata_fields = st.multiselect(
                    "Select fields used as metadata",
                    columns,
                    key="metadata"
                )

            # Initialize session state
            if 'upload_payload' not in st.session_state:
                st.session_state.upload_payload = None

            # Preview button
            if st.button("Preview Data"):
                if not table_name:
                    st.error("Please enter a table name")
                    st.stop()
                
                # Create items list
                items = []
                for _, row in df.iterrows():
                    item = {}
                    for col in columns:
                        value = row[col]
                        if pd.isna(value):
                            value = ""
                        else:
                            value = str(value)
                        item[col] = value
                    items.append(item)
                
                # Store payload in session state
                st.session_state.upload_payload = {
                    "data": {
                        "schema": {
                            "searchableFields": searchable_fields,
                            "metadataFields": metadata_fields
                        },
                        "name": table_name,
                        "items": items
                    }
                }

            # Show preview if available
            if st.session_state.upload_payload:
                st.subheader("📋 Data Preview")
                payload = st.session_state.upload_payload['data']
                
                # Display preview information
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Table Name", payload['name'])
                with col2:
                    st.metric("Total Rows", len(payload['items']))
                
                st.write("Preview of first 3 rows:")
                st.dataframe(df.head(3))

                # Upload button
                if st.button("Upload to Voiceflow"):
                    headers = {
                        "Authorization": VOICEFLOW_API_KEY,
                        "Content-Type": "application/json",
                        "accept": "application/json"
                    }
                    
                    # Send request to Voiceflow API
                    response = requests.post(
                        f"{UPLOAD_URL}?overwrite=true",
                        headers=headers,
                        json=st.session_state.upload_payload
                    )
                    
                    # Handle response
                    if response.status_code == 200:
                        st.success("Upload successful! Your data is now being processed by Voiceflow")
                        st.balloons()
                    else:
                        st.error(f"❌ Upload failed: {response.text}")
        
        except Exception as e:
            st.error(f"⚠️ Error processing file: {str(e)}")

if __name__ == "__main__":
    if not VOICEFLOW_API_KEY:
        st.error("Missing VOICEFLOW_API_KEY in .env file")
    else:
        main()
