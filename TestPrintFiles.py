from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os
import pickle

# Replace with the path to your client secrets file downloaded from Google Cloud Platform
CLIENT_SECRETS_FILE = "C:/Users/kalew/Downloads/client_secret_865603282077-bl69bb6comhvj5sj4o8t2ck86fs54t9d.apps.googleusercontent.com.json"

# Define the desired scopes for your application
SCOPES = ['https://www.googleapis.com/auth/drive']

def get_authenticated_service():
    """
    Establishes user authorization and builds the Drive service object.

    Returns:
        A Google Drive service object if authorization is successful, None otherwise.
    """
    creds = None
    token_path = 'token.pickle'
    if os.path.exists(token_path):
        with open(token_path, 'rb') as token:
            creds = pickle.load(token)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(token_path, 'wb') as token:
            pickle.dump(creds, token)
    
    return build('drive', 'v3', credentials=creds)

def list_folders(service):
    """
    Lists the names of all folders in the user's Drive.

    Args:
        service: The authorized Drive service object.
    """
    query = "mimeType='application/vnd.google-apps.folder'"
    try:
        results = service.files().list(q=query, fields="files(id, name)").execute()
        folders = results.get('files', [])
        
        if folders:
            print("Folders in your Google Drive:")
            for folder in folders:
                print(f'Folder Name: {folder["name"]}')
        else:
            print('No folders found in your Google Drive.')
    except Exception as e:
        print(f'An error occurred while retrieving folders: {e}')

def main():
    """
    Main function to handle authorization and folder listing.
    """
    service = get_authenticated_service()
    if service is not None:
        list_folders(service)

if __name__ == '__main__':
    # Delete the token file to force re-authentication
    if os.path.exists('token.pickle'):
        os.remove('token.pickle')
    main()
