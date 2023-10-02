import os
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Define the scope for Google Drive (full access)
SCOPES = ['https://www.googleapis.com/auth/drive.file']

def authenticate_and_upload():
    # Create or load credentials
    creds = None
    if os.path.exists('token.json'):
        creds = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES).run_local_server(port=0)
        # Save the credentials for future runs
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    else:
        print("No 'token.json' file found. Please create 'credentials.json' and run this script again.")
        return

    # Create a Google Drive service
    service = build('drive', 'v3', credentials=creds)

    local_directory = 'output' 

    # List all files in the local directory
    for root, dirs, files in os.walk(local_directory):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            
            # Upload each file to Google Drive
            media = MediaFileUpload(file_path, resumable=True)
            file_metadata = {'name': file_name}
            uploaded_file = service.files().create(
                media_body=media,
                body=file_metadata,
            ).execute()

            print(f'File uploaded: {uploaded_file["name"]} (ID: {uploaded_file["id"]})')

if __name__ == '__main__':
    authenticate_and_upload()
