# Voiceflow Knowledge Base Uploader

A Streamlit application for uploading Excel/CSV data to Voiceflow's Knowledge Base with field mapping capabilities using VoiceFLow API.

## Project Description

This tool allows you to:
- Upload Excel (.xlsx, .xls) or CSV files
- Map columns to either searchable fields or metadata
- Preview data before uploading
- Set custom table names
- Batch upload to Voiceflow's Knowledge Base

Perfect for:
- Importing FAQ datasets
- Uploading product catalogs
- Creating knowledge bases from spreadsheets
- Migrating existing data to Voiceflow

## Setup Instructions

```bash
# Clone the repository
git clone https://github.com/i-jasmin/VF-API-KBU
cd FF-API-KBU

# Create and activate virtual environment
python -m venv venv

# Windows
.\venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create environment file
echo "VOICEFLOW_API_KEY=your_api_key_here" > .env
```

## Usage

1. Place your Excel/CSV files in the project directory
2. Run the application:
```bash
streamlit run main.py
```
3. In the browser:
   - Upload your file
   - Set table name
   - Configure field mapping
   - Preview and upload

## Requirements

- Python 3.7+
- Voiceflow API key
- Excel/CSV files with headers

## File Structure
```
project/
├── venv/           # Virtual environment
├── main.py          # Main application
├── .env            # API configuration
└── requirements.txt # Dependencies
```

## Notes
- Keep your `.env` file secure
- First row of files should contain headers
- Large files may take time to process