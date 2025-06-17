import os
import io
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle

class GoogleDriveConnector:
    # Initialize the connector
    def __init__(self, credentials_path='credentials.json', token_path='token.pickle'):
        self.credentials_path = credentials_path
        self.token_path = token_path
        self.service = self.authenticate()

    # Authenticate the user
    def authenticate(self):
        print("Starting authentication...")  # debug print
        SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
        creds = None

        if os.path.exists(self.token_path):
            print(f"Loading token from {self.token_path}...")  # debug print
            with open(self.token_path, 'rb') as token:
                creds = pickle.load(token)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                print("Refreshing expired token...")  # debug print
                creds.refresh(Request())
            else:
                print("Running local server for auth...")  # debug print
                flow = InstalledAppFlow.from_client_secrets_file(self.credentials_path, SCOPES)
                creds = flow.run_local_server(port=0)
            with open(self.token_path, 'wb') as token:
                pickle.dump(creds, token)
                print(f"Saved token to {self.token_path}")  # debug print

        service = build('drive', 'v3', credentials=creds)
        print("Google Drive service created.")
        return service

    # List files from google drive   
    def list_files(self, mime_types=None):
        query = ""
        if mime_types:
            mime_query = " or ".join([f"mimeType='{m}'" for m in mime_types])
            query = f"({mime_query})"

        results = self.service.files().list(q=query, pageSize=20, fields="files(id, name, mimeType)").execute()
        files = results.get('files', [])
        return files

    # Download a file from google drive
    def download_file(self, file_id, filename):
        print(f"Downloading file: {filename} (ID: {file_id})")
        request = self.service.files().get_media(fileId=file_id)
        fh = io.FileIO(filename, 'wb')
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while not done:
            _, done = downloader.next_chunk()
        print(f"Downloaded {filename} successfully.")
        return filename


if __name__ == "__main__":
    gdc = GoogleDriveConnector()
    files = gdc.list_files(mime_types=[
        "text/plain",
        "text/csv",
        "application/pdf",
        "image/png"
    ])
    print("Files found:")
    for f in files:
        print(f"{f['name']} ({f['mimeType']}) - ID: {f['id']}")

    if files:
        first_file = files[0]
        gdc.download_file(first_file['id'], first_file['name'])
        
