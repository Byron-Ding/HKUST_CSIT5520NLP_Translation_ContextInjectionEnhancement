import lmstudio as lms
import pathlib
import os
import yaml
import importlib.util
import importlib.machinery
import re
import regex
from typing import Optional
import aiofiles

# regex.DOTALL with \n
result_format_regex: regex.Pattern[str] = regex.compile(r"<output>(.*?)</output>", regex.DOTALL)
# 匹配所有汉字（基本区块 + 扩展区 + 兼容汉字）
all_chinese_characters: regex.Pattern[str] = regex.compile(r'[\u4e00-\u9fff\u3400-\u4dbf\uf900-\ufaff\u20000-\u2a6df\u2a700-\u2b73f\u2b740-\u2b81f\u2b820-\u2ceaf\u2ceb0-\u2ebef]')

# A JSON schema for a book
schema: dict[str, dict[str, dict[str, str]] | str] = {
    "type": "object",
    "properties": {
        "only_one_translate_with_comment": {
            "type": "string",
        },
        "others": {
            "type": "string",
        } 
    }
}

# lmstudio_root_path: pathlib.Path = pathlib.Path(r"F:/.lmstudio/lmstudio-community/")

# ----------------------------------------------- Model Paths ------------------------------------------------
meta_llama_path: str = r"meta-llama-3.1-8b-instruct"
qwen_path: str = r"qwen/qwen3.5-9b"
bytedance_seed_oss_36b_path: str = r"bytedance/seed-oss-36b"

# model = lms.llm(
#     qwen_path,
# )
# result = model.respond(template)

# print(result)

# ----------------------------------------------- Project Paths ------------------------------------------------
# set .. as the root path
project_root_path: pathlib.Path = pathlib.Path(__file__).parent.parent

# load data
data_path = project_root_path / "data" / r"config" / "test.yaml"
# store data
output_data_base_path = project_root_path / "output"

# general template
# import from /data/dataclass/template/general_translate.py
general_translate_module_path = project_root_path / "data" / "dataclass" / "template" / "general_translate.py"



# ------------------------------------------------ Load Data ------------------------------------------------
with open(data_path, "r", encoding="utf-8") as f:
    data = yaml.safe_load(f)

# ------------------------------------------------ Load General Template ------------------------------------------------
spec: Optional[importlib.machinery.ModuleSpec] = importlib.util.spec_from_file_location("general_translate", general_translate_module_path)

if spec is not None and spec.loader is not None:
    general_template_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(general_template_module)

    
general_template: general_translate_module.GeneralTemplate = general_template_module.GeneralTemplate()




# ------------------------------------------------ AI test ------------------------------------------------
async def generate_input(
    model_path: str = qwen_path
):
    async with lms.AsyncClient() as client:
        model = await client.llm.model(
            model_path
        )
        for each_sentence_config in data:
            each_sentence_template: str = each_sentence_config["sentence"]
            each_sentence_keywords: str = each_sentence_config["keywords"]
            each_sentence_summary: str = each_sentence_config["summary"]
            each_sentence_input_language: str = each_sentence_config["input_language"]
            each_sentence_output_language: str = each_sentence_config["output_language"]
            
            if each_sentence_input_language != "en":
                # print(f"Input language {each_sentence_input_language} is not supported yet.")
                continue
                
            for each_keyword in each_sentence_keywords:
                # ---------------- Output path ----------------
                current_output_original_data_path: pathlib.Path = output_data_base_path / \
                    model_path / \
                    each_sentence_summary / \
                    f"{each_keyword}_original.txt"
                current_output_data_path: pathlib.Path = output_data_base_path / \
                    model_path / \
                    each_sentence_summary / \
                    f"{each_keyword}.txt"
                current_output_data_path.parent.mkdir(parents=True, exist_ok=True)
                
                # ---------- Generate input  ----------
                each_sentence = each_sentence_template.format(
                    keyword = each_keyword
                )
                
                synonyms_hint: str = " ".join(each_sentence_keywords) + \
                    "\n" + \
                    "\n".join([
                        general_template.english_synonyms_dictionary_url.format(word=each_keyword) 
                        for each_keyword in each_sentence.split()
                    ])
                
                full_template: str = general_template.format_translate_template(
                    input_text=each_sentence,
                    input_language=each_sentence_input_language,
                    output_language=each_sentence_output_language,
                    input_key_synonyms=synonyms_hint
                )
                
                # [Debug] Print the full template to check if it's correct
                # print(model.get_load_config())
                print(f"Input sentence: {full_template}")
                
                # ----------------------- Get response and stream it -----------------------
                result = await model.respond_stream(
                    full_template
                )
                
                with open(current_output_original_data_path, "w", encoding="utf-8") as f:
                    # Stream the response
                    async for fragment in result:
                        f.write(fragment.content)
                        print(fragment.content, end="", flush=True)
                print()
                print()
                # Note that even for structured responses, the *fragment* contents are still only text
                # Get the final structured result
                complete_result = result.result()
                print(f"Output result: {complete_result}")
                
                real_result = extract_translate_with_comment_from_result(str(complete_result))
                
                if real_result is None:
                    print(f"No valid output found for sentence: {each_sentence}")
                    continue
                else:
                    async with aiofiles.open(current_output_data_path, "w", encoding="utf-8") as f:
                        await f.write(real_result)
                
        
def extract_translate_with_comment_from_result(
    result: str
) -> Optional[str]:
    # get all chinese characters in result
    # remove all english characters, punctuation and numbers
    chinese_characters = regex.findall(all_chinese_characters, result)
    chinese_characters_str = " ".join(chinese_characters)
    
    return chinese_characters_str if chinese_characters_str else None
        
if __name__ == "__main__":
    import asyncio
    asyncio.run(generate_input(
        model_path=qwen_path
        
    ))