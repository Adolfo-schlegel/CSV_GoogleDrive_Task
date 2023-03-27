from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
import os

def make_authorize(SCOPES,TOKEN,CLIEN_SECRET):
        creds = None
        if os.path.exists(TOKEN):
            creds = Credentials.from_authorized_user_file(TOKEN, SCOPES)   
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(CLIEN_SECRET, SCOPES)
                creds = flow.run_local_server(port=0)
            with open(TOKEN, 'w') as token:
                token.write(creds.to_json())                    
        return creds
