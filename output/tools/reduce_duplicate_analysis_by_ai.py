from typing import Optional
import pathlib
import os
import opencc
import yaml

# root path
project_root_path = pathlib.Path(__file__).parent.parent

# data path
data_path = project_root_path / r"qwen/qwen3.5-9b"
# current folder path
current_folder_path = pathlib.Path(__file__).parent


data_path_ls = os.listdir(data_path)

with open(current_folder_path / "config" / "filtered_non_related_word.yaml", "r", encoding="utf-8") as f:
    filtered_non_related_word_data = yaml.safe_load(f)

non_related_word_list = filtered_non_related_word_data[0]
non_related_word_list_dict = non_related_word_list["non_related_words"]
non_related_word_list_general = non_related_word_list_dict["general"]
non_related_word_list_general_contain = non_related_word_list_dict["general_contain"]


for folder in data_path_ls:
    if folder == "tools":
        continue
    
    each_word_responses: list[str] = []
    
    folder_path = data_path / folder
    ls_files = os.listdir(folder_path)
    for file in ls_files:
        print(f"Processing file: {file}")
        if not file.endswith("_reduced_duplicate.txt"):
            continue
        
        file_path = folder_path / file
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        words = content.split()
        filtered_words = []
        for word in words:
            word: str
            if word in non_related_word_list_general:
                continue
            
            if any(non_related_word in word for non_related_word in non_related_word_list_general_contain):
                continue
            
            # 长度小于2的词也过滤掉
            if len(word) < 2:
                continue
            
            # 繁体转简体
            converter = opencc.OpenCC('t2s')
            word = converter.convert(word)
            
            if word not in filtered_words:
                filtered_words.append(word)
        
        # print(f"Filtered words for file {file}: {filtered_words}")
        with open(folder_path / f"{file[:-4]}_analysis_by_ai.txt", "w", encoding="utf-8") as f:
            f.write(" ".join(filtered_words))
            
        