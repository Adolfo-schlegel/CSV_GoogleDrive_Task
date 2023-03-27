
from __future__ import print_function
from ast import Return
from tkinter.messagebox import RETRY
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload, MediaIoBaseUpload
import AuthGD 
import json
import io

with open('parameters.json', 'r') as f:
    data = json.load(f)

API_NAME = data["API_NAME"]
API_VERSION = data["API_VERSION"]
SCOPES = data["SCOPES"]
CREDENTIALS_FILE = data["CREDENTIALS_FILE"]
TOKEN = data["TOKEN"]

class GD:
   
    #Constructor
    def __init__(self):        
        self.creds = AuthGD.make_authorize(
            SCOPES,
            TOKEN,
            CREDENTIALS_FILE)
        self.service = build(API_NAME, API_VERSION, credentials= self.creds)  
          
    def list_files(self):     
        """Lista los archivos de Google Drive."""

        try:         
            results = self.service.files().list(pageSize=10, fields="nextPageToken, files(id, name)").execute()

            items = results.get('files', [])   

            return items 

        except HttpError as error:
            print(f'An error occurred: {error}')

    def list_files_onfolder(self,folder = 'root'):     
         """Lista los archivos de Google Drive en una carpeta."""

         try:
             folder_id = self.search_drive_files(folder)
             query = "'{}' in parents and trashed=false".format(folder_id)

             results = self.service.files().list(q=query, fields="nextPageToken, files(name)").execute()
             items = results.get('files', [])
             
             if len(items) > 0:
                return items[0]['name']
             else:
                 return "File not found"

         except HttpError as error:
             print (f"An error occurred: {error}")
             return None
         

    def create_folder(self,name):
        """Crea uan carpeta a Google Drive."""
        try:
            
            folder_id = self.search_drive_files(name)

            if(folder_id != None):
                return folder_id

            file_metadata = {
                'name': name,
                'mimeType': 'application/vnd.google-apps.folder'
            }
            
            file = self.service.files().create(body=file_metadata, fields='id').execute()

            print(F'Folder ID: "{file.get("id")}".')
            
            return "Folder created -> ",file.get('id')

        except HttpError as error:
            print(F'An error occurred: {error}')
            return None
    
    def upload_basic(self,filePath,folder_repo):     
        """Sube un archivo a Google Drive."""

        try:        

           folder_id = self.search_drive_files(folder_repo)

           if(id == None):
              return None

           file_metadata = {
               'name': filePath,
               'parents': [folder_id]
           }

           media = MediaFileUpload(filePath, mimetype='text/csv')
    
           file = self.service.files().create(body=file_metadata, media_body=media, fields='id').execute()

           print(F'File ID: {file.get("id")}')  
                    
           return "File Created -> ", file.get('id')    
        except HttpError as error:
            print(F'An error occurred: {error}')
            file = None

    def exist_file(self,file_name):

        query = "name='{}' and trashed=false".format(file_name)
        try:
            results = self.service.files().list(q=query, fields="nextPageToken, files(id, name)").execute()
            items = results.get('files', [])
            
            if len(items) <= 0:
                return False   
            
            return True                   
        except HttpError as error:
            return None

    def update_file(self,old_filename, new_filename, drive_folder, mimetype='text/csv'):

         try:

            # Step 1: Id folder 
            folder_id = self.search_drive_files(drive_folder)

            # Step 2: Id file 
            file_id = self.search_drive_files(old_filename,folder_id)
            
            # Step 3: Update the file with the new content
            file_metadata = {'name': f'{new_filename}'}
            media = MediaIoBaseUpload(io.BytesIO(b'New content'), mimetype=f'{mimetype}', chunksize=1024*1024, resumable=True)

            updated_file = self.service.files().update(fileId=file_id, body=file_metadata, media_body=media, fields='id').execute()
            
            return "File updated: %s" % updated_file.get('id')

         except HttpError as error:
             print (f"An error occurred: {error}")
             return None

    def search_drive_files(self,file_name,folder_id = 'root'):
         """
         Busca el ID de un archivo en Google Drive por su nombre.

         Args:
             file_name (str): Nombre del archivo a buscar.

         Returns:
             str: ID del archivo si se encuentra, None en caso contrario.
         """

         try:
             # Buscar el archivo por nombre
             query = f"name='{file_name}' and trashed=false and '{folder_id}' in parents "
             results = self.service.files().list(q=query, fields="nextPageToken, files(id)").execute()
             items = results.get('files', [])

             # Obtener el ID del primer archivo encontrado
             if items:
                 return items[0]['id']
             else:
                 return None
    
         except HttpError as error:
            print(f"Ocurrio un error: {error}")
            return None

    def download_file(self, nombre_archivo):
         """Descarga un archivo de Google Drive."""

         id_archivo = self.search_drive_files(nombre_archivo)
         if(id == None):
            return None

         try:
             request = self.service.files().get_media(fileId=id_archivo)

             fh = io.BytesIO()

             downloader = MediaIoBaseDownload(fh, request)

             done = False
             while done is False:
                 status, done = downloader.next_chunk()

                 print(f"Descargado {int(status.progress() * 100)}.")
             with open(nombre_archivo, 'wb') as f:
                 f.write(fh.getvalue())
             print(f"El archivo '{nombre_archivo}' se descargo correctamente.")
         except HttpError as error:
             print(f"Ocurrio un error al descargar el archivo: {error}")



