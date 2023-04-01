import GenerateCSV
import json
from GoogleDriveClientPython import GD as GoogleDrive

# Open the JSON file in read mode and load it into a Python object
with open('parameters.json', 'r') as f:
    data = json.load(f)

folder_name = data['folder_name']
file_name = data['name_file']


#Get history of bitcoin
result = GenerateCSV.CreateCsvFile()

if result == "OK" :     

     print("El CSV se ha guardado correctamente.")

     DriveService = GoogleDrive()

     result = DriveService.create_folder(folder_name)
     old_filename = DriveService.list_files_onfolder(folder_name)

     if(result != None):
         if not(DriveService.exist_file(file_name) or DriveService.exist_file(old_filename)):
             resultFile = DriveService.upload_basic(file_name, folder_name)
         else : 
             resultFile = DriveService.update_file(old_filename, file_name,folder_name)               
     print(resultFile)

input("Press Enter to continue...")

#def case_1():
#   lst_files = DriveService.list_files()
        
#   for item in lst_files:
#        print(u'{0} ({1})'.format(item['name'], item['id'])) 

#def case_2():
#    print("Increse el path del archivo :")
#    path = input("->")

#    resultFile = DriveService.upload_basic(path)
#    print(resultFile)

#def case_2():
#    print("Increse el nombre de la carpeta :")
#    name_folder = input("->")

#    resultFile = DriveService.create_folder(name_folder)
#    print(resultFile)

#def case_2():
#    print("Increse el nombre del archivo que quiere descargar:")
#    name_file= input("->")

#    resultFile = DriveService.download_file(name_file)
#    print(resultFile)
 
#opciones = {
#    1: case_1,
#    2: case_2,
#}

#if result == "OK" :     
#     print("El CSV se ha guardado correctamente.")

#     print("Selecciona una opcion: ")

#     while(True):
#        print("\n1) Listar archivos")
#        print("2) Subir un archivo")        
#        print("3) Crear una carpeta")
#        print("4) Descargar un archivo")

#        opcion = input("->")
         
#        opciones.get(int(opcion))()
     


