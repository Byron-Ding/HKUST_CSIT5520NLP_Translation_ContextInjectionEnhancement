import textdistance
import pathlib
import os
import itertools

# root path
project_root_path = pathlib.Path(__file__).parent.parent

# data path
data_path = project_root_path / "output" / "qwen" / "qwen3.5-9b"


data_path_ls = os.listdir(data_path)




# 选择算法，例如 Jaccard
sim_func = textdistance.cosine.similarity

for folder in data_path_ls:
    if folder == "tools":
        continue
    
    each_word_responses: list[str] = []
    
    folder_path = data_path / folder
    ls_files = os.listdir(folder_path)
    for file in ls_files:
        if "_reduced_duplicate" not in file:
            continue
        
        file_path = folder_path / file
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        each_word_responses.append(content)
        
    pairs_similarity = list(
        itertools.combinations(each_word_responses, 2)
    )

    sims = [sim_func(pair[0], pair[1]) for pair in pairs_similarity]
    
    avg_similarity = sum(sims) / len(sims) if sims or len(sims) != 0 else 0
    print(f"Folder: {folder}, Average Similarity: {avg_similarity}")
    # print("平均相似度:", avg_similarity)
