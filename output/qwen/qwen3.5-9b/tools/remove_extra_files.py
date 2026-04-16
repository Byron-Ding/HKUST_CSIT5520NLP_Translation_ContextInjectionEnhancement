import os
import pathlib

# root path
project_root_path = pathlib.Path(__file__).parent.parent



for folder in os.listdir(project_root_path):
    if folder == "tools":
        continue
    
    folder_path = os.path.join(project_root_path, folder)
    ls_files = os.listdir(folder_path)
    for file in ls_files:
        if ".txt_" in file:
            file_path = os.path.join(folder_path, file)
            os.remove(file_path)