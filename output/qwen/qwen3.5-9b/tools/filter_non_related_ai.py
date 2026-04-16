import pathlib
from sentence_transformers import SentenceTransformer, util
import yaml
import torch

# 检查是否有 GPU
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using device: {device}")

# 加载模型到指定设备
model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2', device=device)


# data path
data_path = pathlib.Path(__file__).parent.parent
project_root_path = data_path.parent.parent.parent
data_config_path = project_root_path / "data" / "config" / "test.yaml"


# load data
with open(data_config_path, "r", encoding="utf-8") as f:
    data = yaml.safe_load(f)
    
dir_appendix: list[str] = ["", "_baseline", "_without_synonyms", "_with_synonyms_but_no_rules"]

for each_sentence_config in data:
    each_sentence_keywords: str = each_sentence_config["keywords"]
    each_sentence_summary: str = each_sentence_config["summary"]
    
    each_sentence_summary_directory = data_path / each_sentence_summary

    # 4 types,
    for each_dir_appendix in dir_appendix:
        each_sentence_summary_directory_with_appendix = \
            each_sentence_summary_directory.with_name(
                each_sentence_summary_directory.name + each_dir_appendix
        )

        # 比较每个文件夹下的文件
        for each_file in each_sentence_summary_directory_with_appendix.iterdir():
            # print(f"Comparing files in directory: {each_word_type_folder}")
            if each_file.is_file() and each_file.name.endswith("_reduced_duplicate.txt"):
                with open(each_file, "r", encoding="utf-8") as f:
                    content = f.read()
                    
                # split by _, the first item is the 
                    
                content_list = content.split()
                
                for each_output_word in content_list:
                    
                    
                    # 批量编码
                    content_embeddings = model.encode(content_list, convert_to_tensor=True, normalize_embeddings=True)
                    keywords_embeddings = model.encode(each_sentence_keywords, convert_to_tensor=True, normalize_embeddings=True)

                    # 计算相似度矩阵
                    similarity_matrix = util.cos_sim(content_embeddings, keywords_embeddings)

                    # 输出每个词的平均相似度
                    for i, word in enumerate(content_list):
                        avg_score = similarity_matrix[i].mean().item()
                        print(f"Similarity between '{word}' and keywords '{each_sentence_keywords}' is {avg_score:.4f}")