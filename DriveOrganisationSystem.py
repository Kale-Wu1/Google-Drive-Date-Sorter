from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os
import pickle

# Replace with the path to your client secrets file downloaded from Google Cloud Platform
CLIENT_SECRETS_FILE = "C:/Users/kalew/Downloads/client_secret_865603282077-bl69bb6comhvj5sj4o8t2ck86fs54t9d.apps.googleusercontent.com.json"

# Define the desired scopes for your application
SCOPES = ['https://www.googleapis.com/auth/drive']

#Get drive service object
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


#Creates a new folder in the user's Drive.
def create_folder(service, folder_name):
  file_metadata = {
      'name': folder_name,
      'mimeType': 'application/vnd.google-apps.folder'
  }
  try:
      folder = service.files().create(body=file_metadata, fields='id').execute()
      print(f'Folder ID: {folder.get("id")}')
      return folder.get('id')
  except Exception as e:
      print(f'An error occurred: {e}')
      return None



#Retrieves a list of file objects within a specified folder.
def get_file_list(service, folder_id):
  query = f"'{folder_id}' in parents"
  try:
      results = service.files().list(q=query, fields="files(id, name)").execute()
      return results.get('files', [])
  except Exception as e:
      print(f'An error occurred while retrieving files: {e}')
      return None



#Moves a file to a new location (specified by destination folder ID).
def move_file(service, file_id, destination_folder_id):
  try:
      file = service.files().update(fileId=file_id, body={'parents': [destination_folder_id]}).execute()
      print(f'Moved file: {file.get("name")}')
  except Exception as e:
      print(f'An error occurred while moving file: {e}')



#Returns modified date of specified file
def get_file_date(service, file_id): 
    try:
       file_metadata = service.files().get(fileId=file_id, fields="modifiedTime").execute()
    
    except Exception as e:
        print(f'An error occurred while retrieving file metadata: {e}')
        return None
    
    if file_metadata:
        modified_date = file_metadata.get('modifiedTime')
        print(f'File creation date: {modified_date}')
        return modified_date
    else:
        print('File not found or error retrieving metadata.')



#Searches for a folder by name and returns its ID (if found).
def get_folder_id_by_name(service, folder_name):
  query = f"mimeType='application/vnd.google-apps.folder' and name = '{folder_name}'"
  try:
      results = service.files().list(q=query, fields="files(id)").execute()
      files = results.get('files', [])
      
      if files:
          return files[0].get('id')
      else:
          print(f'Folder "{folder_name}" not found.')
          return None
  except Exception as e:
      print(f'An error occurred while retrieving folder: {e}')
      return None

def main():
  service = get_authenticated_service()
  

  if service is not None:

    print(service.files().list(q=f"mimeType='application/vnd.google-apps.folder'", fields="files(name)").execute())
    

    # Replace with IDs of your source and destination folders
    source_folder_id = get_folder_id_by_name(service, "NewFolder")
    #destination_folder_id = 'your_destination_folder_id'

    files = get_file_list(service, source_folder_id)
    print(files)
    if files:
        for file_info in files:
          print(file_info['id'] + " has a modification date of " + get_file_date(service, file_info['id']))
    else:
      print('No files found in the source folder.')

    


if __name__ == '__main__':
  main()