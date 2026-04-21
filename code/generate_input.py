import lmstudio as lms
import pathlib
import yaml
import regex
from typing import Optional, Callable
from typing import TypeIs
import aiofiles
import sys
import inspect

# set the root path and chdir to the root path
project_root = pathlib.Path(__file__).parent.parent
sys.path.append(str(project_root))



# Type checking
# check Callable[[str, str, str, str], str] and Callable[[str, str, str], str]
def is_callable_with_4_args(func: Callable[..., str]) -> TypeIs[Callable[[str, str, str, str], str]]:
    function_information: inspect.FullArgSpec = inspect.getfullargspec(func)
    return len(function_information.args) == 4

def is_callable_with_3_args(func: Callable[..., str]) -> TypeIs[Callable[[str, str, str], str]]:
    function_information: inspect.FullArgSpec = inspect.getfullargspec(func)
    return len(function_information.args) == 3






from data.dataclass.template import general_translate as general_translate_module

# regex.DOTALL with \n
result_format_regex: regex.Pattern[str] = regex.compile(r"<output>(.*?)</output>", regex.DOTALL)
# 匹配所有非汉字字符
all_non_chinese_characters: regex.Pattern[str] = regex.compile(r"[^\p{Han}]")

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
data_path = project_root_path / r"data" / r"source" / r"synonyms_data.yaml"
# store data
output_data_base_path = project_root_path / r"output"

# general template
# import from /data/dataclass/template/general_translate.py
general_translate_module_path = project_root_path / r"data" / r"dataclass" / r"template" / r"general_translate.py"



# ------------------------------------------------ Load Data ------------------------------------------------
with open(data_path, "r", encoding="utf-8") as f:
    data = yaml.safe_load(f)

# ------------------------------------------------ Load General Template ------------------------------------------------
# spec: Optional[importlib.machinery.ModuleSpec] = importlib.util.spec_from_file_location("general_translate", general_translate_module_path)

# if spec is not None and spec.loader is not None:
#     general_template_module = importlib.util.module_from_spec(spec)
#     spec.loader.exec_module(general_template_module)

    
general_template: general_translate_module.GeneralTemplate = general_translate_module.GeneralTemplate()


    
# ------------------------------------------------ AI test ------------------------------------------------
async def generate_input(
    input_generation_function: Callable[
        ..., str
    ],
    model_path: str = qwen_path,
) -> None:
    # ------------------------ Initialize client and model -----------------------
    async with lms.AsyncClient() as client:
        model = await client.llm.model(
            model_path
        )
        # ------------------------ Iterate through data and generate input -----------------------
        for each_sentence_config in data:
            each_sentence_template: str = each_sentence_config["sentence"]
            each_sentence_keywords: str = each_sentence_config["keywords"]
            each_sentence_summary: str = each_sentence_config["summary"]
            each_sentence_input_language: str = each_sentence_config["input_language"]
            each_sentence_output_language: str = each_sentence_config["output_language"]
            
            
            # ---------------- Currently only Test English input ----------------
            if each_sentence_input_language != "en":
                # print(f"Input language {each_sentence_input_language} is not supported yet.")
                continue
                
            for each_keyword in each_sentence_keywords:
                # ---------------- Output path ----------------
                each_sentence_summary_without_synonyms = each_sentence_summary + r"_with_synonyms_but_no_rules"
                current_output_original_data_path: pathlib.Path = output_data_base_path / \
                    model_path / \
                    each_sentence_summary_without_synonyms / \
                    f"{each_keyword}_original.txt"
                current_output_data_path: pathlib.Path = output_data_base_path / \
                    model_path / \
                    each_sentence_summary_without_synonyms / \
                    f"{each_keyword}.txt"
                current_output_data_path.parent.mkdir(parents=True, exist_ok=True)
                
                # ---------- Generate input  ----------
                each_sentence: str = each_sentence_template.format(
                    keyword = each_keyword
                )
                
                synonyms_hint: str = " ".join(each_sentence_keywords) + \
                    "\n" + \
                    "\n".join([
                        general_template.english_synonyms_dictionary_url.format(word=each_keyword) 
                        for each_keyword in each_sentence.split()
                    ])
                
                
                full_template: str
                if is_callable_with_4_args(input_generation_function):
                    full_template: str = input_generation_function(
                        each_sentence,
                        each_sentence_input_language,
                        each_sentence_output_language,
                        synonyms_hint,
                    )
                elif is_callable_with_3_args(input_generation_function):
                    full_template: str = input_generation_function(
                        input_text=each_sentence,
                        input_language=each_sentence_input_language,
                        output_language=each_sentence_output_language,
                    )
                else:
                    raise ValueError("Input generation function must have either 3 or 4 arguments.")
                
                # [Debug] Print the full template to check if it's correct
                # print(model.get_load_config())
                print(f"Input sentence: {full_template}")
                
                # ----------------------- Get response and stream it -----------------------
                result = await model.respond_stream(
                    full_template
                )
                print(f"[Debug] File path for original output: {current_output_original_data_path}")
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
    chinese_characters = regex.sub(all_non_chinese_characters, r" ", result)
    
    chinese_characters = regex.sub(r"\s+", " ", chinese_characters).strip()
    
    return chinese_characters if chinese_characters else None
        
        
if __name__ == "__main__":
    import asyncio
    
    asyncio.run(generate_input(
        general_translate_module.GeneralTemplate.format_translate_template_with_synonyms_with_rules,
        model_path=qwen_path
    ))
    asyncio.run(generate_input(
        general_translate_module.GeneralTemplate.format_translate_template_no_synonyms_no_rules,
        model_path=qwen_path
    ))
    asyncio.run(generate_input(
        general_translate_module.GeneralTemplate.format_translate_template_with_synonyms_no_rules,
        model_path=qwen_path
    ))
    asyncio.run(generate_input(
        general_translate_module.GeneralTemplate.format_translate_template_no_synonyms_with_rules,
        model_path=qwen_path
    ))