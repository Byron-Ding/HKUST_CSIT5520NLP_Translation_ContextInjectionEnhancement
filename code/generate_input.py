import lmstudio as lms
import pathlib
import os
import yaml
import importlib.util
import importlib.machinery
import re
from typing import Optional
import aiofiles

# re.DOTALL with \n
result_format_regex: re.Pattern = re.compile(r"<output>(.*?)</output>", re.DOTALL)

# A JSON schema for a book
schema = {
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

meta_llama_path: str = r"meta-llama-3.1-8b-instruct"
qwen_path: str = r"qwen/qwen3.5-9b"
bytedance_seed_oss_36b_path: str = r"bytedance/seed-oss-36b"

# model = lms.llm(
#     qwen_path,
# )
# result = model.respond(template)

# print(result)

# set .. as the root path
project_root_path: pathlib.Path = pathlib.Path(__file__).parent.parent

# load data
data_path = project_root_path / "data" / r"config" / "test.yaml"
# store data
output_data_base_path = project_root_path / "output"

with open(data_path, "r", encoding="utf-8") as f:
    data = yaml.safe_load(f)


# general template
# import from /data/dataclass/template/general_translate.py
general_translate_module_path = project_root_path / "data" / "dataclass" / "template" / "general_translate.py"

spec: Optional[importlib.machinery.ModuleSpec] = importlib.util.spec_from_file_location("general_translate", general_translate_module_path)

if spec is not None and spec.loader is not None:
    general_template_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(general_template_module)
    
general_template: general_translate_module.GeneralTemplate = general_template_module.GeneralTemplate()

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
                
                # print(model.get_load_config())
                
                print(f"Input sentence: {full_template}")
                result = await model.respond_stream(
                    full_template
                )
                # Stream the response
                async for fragment in result:
                    print(fragment.content, end="", flush=True)
                print()
                # Note that even for structured responses, the *fragment* contents are still only text
                # Get the final structured result
                result_result = result.result()
                
                print(f"Output result: {result_result}")
                
                current_output_data_path = output_data_base_path / model_path / each_sentence_summary / f"{each_keyword}.txt"
                current_output_data_path.parent.mkdir(parents=True, exist_ok=True)
                
                real_result = extract_translate_with_comment_from_result(str(result))
                
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
    chinese_characters = re.sub(r"[a-zA-Z0-9\<\>\[\]\(\)\{\}\s\n\r]", "", result)
    return chinese_characters if chinese_characters else None
        
if __name__ == "__main__":
    import asyncio
    asyncio.run(generate_input(
        model_path=qwen_path
        
    ))