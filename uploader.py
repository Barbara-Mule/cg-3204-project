import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Set your credentials file
CREDENTIALS_FILE = 'credentials.json'

# Set the local directory containing the files you want to upload
LOCAL_DIRECTORY = 'output'

FOLDER_ID = None

# Create a Google Drive service
def create_drive_service():
    credentials = service_account.Credentials.from_service_account_file(
        CREDENTIALS_FILE,
        scopes=['https://www.googleapis.com/auth/drive']
    )
    drive_service = build('drive', 'v3', credentials=credentials)
    return drive_service

# Upload files from the local directory to Google Drive
def upload_files_to_drive():
    drive_service = create_drive_service()

    for filename in os.listdir(LOCAL_DIRECTORY):
        if os.path.isfile(os.path.join(LOCAL_DIRECTORY, filename)):
            file_metadata = {
                'name': filename,
                'parents': [FOLDER_ID]
            }
            media = MediaFileUpload(
                os.path.join(LOCAL_DIRECTORY, filename),
                resumable=True
            )

            uploaded_file = drive_service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id'
            ).execute()

            print(f'Uploaded file: {filename}, File ID: {uploaded_file["id"]}')

if __name__ == '__main__':
    upload_files_to_drive()
