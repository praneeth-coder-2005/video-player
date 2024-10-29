import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from config import GOOGLE_CREDENTIALS

def initialize_drive_api():
    creds = service_account.Credentials.from_service_account_file(
        GOOGLE_CREDENTIALS, scopes=["https://www.googleapis.com/auth/drive.file"]
    )
    return build('drive', 'v3', credentials=creds)

def upload_file_to_drive(file_path, file_name, folder_id):
    drive_service = initialize_drive_api()
    file_metadata = {
        'name': file_name,
        'parents': [folder_id]
    }
    media = MediaFileUpload(file_path, resumable=True)
    file = drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    return file.get('id')
