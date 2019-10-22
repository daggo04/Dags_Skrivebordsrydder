#Modules
from watchdog.observers import Observer
import time
from watchdog.events import FileSystemEventHandler
import os 
import json
import shutil
from datetime import datetime
from time import gmtime, strftime
#Data
from file_folders_data import extensions_folders, excepted_filenames, spesific_filehandling

class Dekstop_Handler(FileSystemEventHandler):
    def on_modified(self, event):
        for filename in os.listdir(folder_to_track):
            i = 0
            if filename not in excepted_filenames:
                # try:
                    new_name = filename
                    extension = 'noname'
                    try:
                        extension = str(os.path.splitext(folder_to_track + '/' + filename)[1]).lower()
                        path = extensions_folders[extension]
                    except Exception:
                        extension = 'noname'

                    now = datetime.now()
                    year = now.strftime("%Y")
                    #Folder and Sepcific filename handling 
                    if os.path.isdir(folder_to_track + "/" + filename):
                        extension = "Folder"
                    for spesific_filename in spesific_filehandling:
                        if filename.startswith(spesific_filename):
                            folder_destination_path = extensions_folders[spesific_filename]
                            break
                        else:
                            folder_destination_path = extensions_folders[extension]
                    #Year folder creation
                    year_exists = False
                    for folder_name in os.listdir(folder_destination_path):
                        if folder_name == year:
                            folder_destination_path = folder_destination_path + "/" +year
                            year_exists = True
                    if not year_exists:
                        os.mkdir(folder_destination_path + "/" + year)
                        folder_destination_path = folder_destination_path + "/" + year
                    #File exist detection and handling
                    file_exists = os.path.isfile(folder_destination_path + "/" + new_name) or os.path.isdir(folder_destination_path + "/" + new_name)
                    while file_exists:
                        i += 1
                        new_name = os.path.splitext(folder_to_track + '/' + filename)[0] + "(" + str(i) + ")" + os.path.splitext(folder_to_track + '/' + filename)[1]
                        new_name = new_name.split("/")[-1]
                        file_exists = os.path.isfile(folder_destination_path + "/" + new_name)
                    src = folder_to_track + "/" + filename

                    new_name = folder_destination_path + "/" + new_name
                    os.rename(src, new_name)
                    print("Moved file: " + os.path.basename(src) + "\nTo: " + folder_destination_path)
                # except Exception:
                #     print(filename)

#Folder Creation
folder_paths = []
for path in extensions_folders.values():
  if path not in folder_paths:
    folder_paths.append(path)
for path in folder_paths:
    if os.path.exists(path) != True:
        os.makedirs(path, exist_ok=True)
        print("Created folder: " + os.path.basename(path) +  " at: " + path)

#Execution
folder_to_track = '/Users/Dag/Desktop'
folder_destination = '/Users/Dag/Desktop'
event_handler = Dekstop_Handler()
observer = Observer()
observer.schedule(event_handler, folder_to_track, recursive=True)
observer.start()
#ASCII Display 
print(r"""
      _                  _             
     | |                (_)            
  ___| | ___  __ _ _ __  _ _ __   __ _ 
 / __| |/ _ \/ _` | '_ \| | '_ \ / _` |
| (__| |  __/ (_| | | | | | | | | (_| |
 \___|_|\___|\__,_|_| |_|_|_| |_|\__, |
                                  __/ |
                                 |___/ 
            """)

#Launch and Shutdown
try:
    while True:           
        time.sleep(10)
except KeyboardInterrupt:
    observer.stop()
observer.join()