from typing import Optional
import regex

# 匹配所有非汉字字符
all_non_chinese_characters: regex.Pattern[str] = regex.compile(r"[^\p{Han}]")

def extract_translate_with_comment_from_result(
    result: str
) -> Optional[str]:
    # get all chinese characters in result
    # remove all english characters, punctuation and numbers
    chinese_characters = regex.sub(all_non_chinese_characters, r" ", result)
    
    return chinese_characters if chinese_characters else None
        
        
# ../重要/word_original.txt

if __name__ == "__main__":
    import asyncio
    import os 
    
    correction_path_base = os.path.join(os.path.dirname(__file__), "..", "开心")
    ls_files = os.listdir(correction_path_base)
    
    for file in ls_files:
        if "_" not in file:
            continue
        file_path = os.path.join(correction_path_base, file)
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        corrected_content = extract_translate_with_comment_from_result(content)
        
        corrected_content = regex.sub(r"\s+", " ", str(corrected_content)).strip()
        
        print(corrected_content)
        
        corresponding_output_file = file.replace("_original", "")
        
        with open(os.path.join(correction_path_base, corresponding_output_file), "w", encoding="utf-8") as f:
            f.write(corrected_content)