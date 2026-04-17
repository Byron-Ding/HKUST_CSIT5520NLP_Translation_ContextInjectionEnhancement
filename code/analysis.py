import textdistance
import pathlib
import os
import itertools
import regex
# 判断中文
def is_chinese_char(string: str) -> bool:
    if regex.match(r"[\p{Han}]", string):
        return True

# root path
project_root_path = pathlib.Path(__file__).parent.parent

# data path
data_path = project_root_path / "output" / "qwen" / "qwen3.5-9b"


data_path_ls = os.listdir(data_path)

output_data_path = project_root_path / "result" / "analysis_results.csv"

# 测试文件夹是否存在，不存在则error提示
if not data_path.exists():
    raise FileNotFoundError(f"Data path {data_path} does not exist.")
# 表头
with open(output_data_path, "w", encoding="utf-8") as f:
    f.write("WordType,Condition,AverageSimilarity,WordNumber,AverageNonSimilarWordLength\n")



    # 选择算法，例如 Jaccard
    sim_func = textdistance.cosine.similarity

    for folder in data_path_ls:
        if folder == "tools":
            continue
        
        each_word_responses: list[str] = []
        average_word_length = 0
        
        folder_path = data_path / folder
        ls_files = os.listdir(folder_path)
        for file in ls_files:
            if not file.endswith("_reduced_duplicate.txt"):
                continue
            
            file_path = folder_path / file
            with open(file_path, "r", encoding="utf-8") as each_word_output_data:
                content = each_word_output_data.read()
                average_word_length += len(content.split())
                
            each_word_responses.append(content)
            
        average_word_length = average_word_length / len(ls_files) if ls_files else 0
            
        pairs_similarity = list(
            itertools.combinations(each_word_responses, 2)
        )

        sims = [sim_func(pair[0], pair[1]) for pair in pairs_similarity]
        
        average_similarity = sum(sims) / len(sims) if sims or len(sims) != 0 else 0
        print(f"Folder: {folder}, Average Similarity: {average_similarity}, Word Number: {average_word_length}")
        
        # 分割，直到遇到不是中文的字符为止，取第一个部分作为词类型，剩下的部分作为条件
        split_result = regex.split(r"_(?=\P{Han})", folder)
        word_type = split_result[0]
        condition = "_".join(split_result[1:]) if len(split_result) > 1 else ""
        print(f"Word type: {word_type}")
        match condition:
            case "baseline":
                condition = "No Synonyms; No Rules"
            case "with_synonyms_but_no_rules":
                condition = "With Synonyms; No Rules"
            case "without_synonyms":
                condition = "No Synonyms; With Rules"
            case "":
                condition = "With Synonyms; With Rules"
            case _:
                condition = condition.replace("_", " ").title()
        
        print(f"Condition: {condition}")
        print(f"Average similarity: {average_similarity}")
        print(f"Average word length: {average_word_length}")
        
        # 算法：最不相似的长度 = (1 - 平均相似度) * 平均词长度
        # 这个才是有长度变化的情况下的差异大小
        average_non_similar_word_length = (1 - average_similarity) * average_word_length
        print(f"Average word length after multiplying with average similarity: {average_non_similar_word_length}")
        
        
        
        f.write(f"{word_type},{condition},{average_similarity},{average_word_length},{average_non_similar_word_length}\n")

    