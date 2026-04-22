from typing import Optional
import pathlib
import os
import jieba

# root path
project_root_path = pathlib.Path(__file__).parent.parent / r"qwen/qwen3.5-9b"

# data path
data_path = project_root_path


data_path_ls = os.listdir(data_path)


for folder in data_path_ls:
    if folder == "tools":
        continue
    
    each_word_responses: list[str] = []
    
    folder_path = data_path / folder
    ls_files = os.listdir(folder_path)
    for file in ls_files:
        print(f"Processing file: {file}")
        if "_" in file:
            continue
        
        file_path = folder_path / file
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        reduced_duplicate_text: list[str] = list(jieba.cut(content, cut_all=False))
        
        reduced_duplicate_text = list(set(reduced_duplicate_text))
        reduced_duplicate_text.sort()
        
        with open(folder_path / f"{file[:-4]}_reduced_duplicate.txt", "w", encoding="utf-8") as f:
            f.write(" ".join(reduced_duplicate_text))
            
        