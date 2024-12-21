from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from google.oauth2.service_account import Credentials
import json
import io
import os
import pandas as pd
import streamlit as st
from sqlalchemy import create_engine




# SERVICE ACCOUNT INFO
# Path to your service account JSON key file
SERVICE_ACCOUNT_FILE = json.loads(os.getenv("GOOGLE_APPLICATION_CREDENTIALS_JSON"))

# Define the scope
SCOPES = ['https://www.googleapis.com/auth/drive.file']

# Authenticate and build the service
credentials = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
drive_service = build('drive', 'v3', credentials=credentials)






# List files in the Google Drive folder (or root, if not specific folder)
response = drive_service.files().list(
    pageSize=1,  # Assume only one file
    fields="files(id, name)"
).execute()

# Get the file details
files = response.get('files', [])
if not files:
    raise Exception("No files found in the Drive.")

# Assuming only one file exists
file = files[0]
file_id = file.get('id')
print(f"Found file: {file['name']} (ID: {file_id})")

# Request to download the file
request = drive_service.files().get_media(fileId=file_id)
file_stream = io.BytesIO()
downloader = MediaIoBaseDownload(file_stream, request)

done = False
while not done:
    status, done = downloader.next_chunk()

# Move the pointer to the beginning of the file stream
file_stream.seek(0)

# Read the CSV file into a pandas DataFrame
df = pd.read_csv(file_stream)








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
    (df["current_total_price"] >= price_filter[0]) &
    (df["current_total_price"] <= price_filter[1]) &
    ((df["disposition"] == disposition_filter) if disposition_filter != "All" else True)
]

# Display Filtered DataFrame
st.dataframe(filtered_df)