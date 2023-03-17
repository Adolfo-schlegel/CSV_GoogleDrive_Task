from __future__ import print_function
import os.path
import bitcoin 
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']

def make_authorize():
    creds = None
    
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('client_secret_1059549673501-41b5ad42bvc382nd783br7omu004qtts.apps.googleusercontent.com.json', SCOPES)   
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secret_1059549673501-41b5ad42bvc382nd783br7omu004qtts.apps.googleusercontent.com.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())               
    return creds

def list_files():     
    
    try:
        creds = make_authorize()   
        service = build('drive', 'v3', credentials=creds)        
        results = service.files().list(pageSize=10, fields="nextPageToken, files(id, name)").execute()
        items = results.get('files', [])   

        for item in items:
            print(u'{0} ({1})'.format(item['name'], item['id']))  

    except HttpError as error:
        print(f'An error occurred: {error}')

def create_folder():
    
    try:
        creds = make_authorize()
        service = build('drive', 'v3', credentials=creds)
        file_metadata = {
            'name': 'Invoices',
            'mimeType': 'application/vnd.google-apps.folder'
        }
        
        file = service.files().create(body=file_metadata, fields='id'
                                      ).execute()
        print(F'Folder ID: "{file.get("id")}".')
        
        return file.get('id')
    except HttpError as error:
        print(F'An error occurred: {error}')
        return None

def upload_basic():     
       
    try:        
       creds = make_authorize()
       service = build('drive', 'v3', credentials=creds)
       file_metadata = {'name': 'download.jpeg'}
       media = MediaFileUpload('download.jpeg', mimetype='image/jpeg')

       file = service.files().create(body=file_metadata, media_body=media,
                                     fields='id').execute()
       print(F'File ID: {file.get("id")}')  
                
       return file.get('id')    
    except HttpError as error:
        print(F'An error occurred: {error}')
        file = None
        
    


