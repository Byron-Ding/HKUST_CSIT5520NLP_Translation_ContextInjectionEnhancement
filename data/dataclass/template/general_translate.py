import dataclasses
from typing import Final

@dataclasses.dataclass(frozen=True)
class GeneralTemplate:
    
    translate_template: Final[str] = """
{input_key_synonyms}
------------------------------------------------------------------
Input-Output-Task: Translate
Input: {input_text}
Input-language: {input_language}
Output-language: {output_language}
Output:

------------------------------------------------------------------
Rules:
1. Allow optional comments, after Each word;
    comments should |point out> the key characteristic/original meaning |of> each word
Output format:
Note: each "(comment)" |is> optional
    "The (comment) project (comment) is (comment)....." 
Note: Output and Comment |are> in Output-Language
3. Compare the similar word of each word -> |point out> the key characteristic |of> each word
4. Characteristic |based on> the original meaning, the original meaning, the original meaning, the original meaning, optional for evolute to the extension |of> each word;
    original meaning |is> important.
5. |Annotate> the original meaning in the comment, which shown |as/in> the output language
    """
    
    
    @staticmethod
    def format_translate_template(
        input_text: str,
        input_language: str,
        output_language: str,
        input_key_synonyms: str = "",
    ) -> str:
        return GeneralTemplate.translate_template.format(
            input_text=input_text,
            input_language=input_language,
            output_language=output_language,
            input_key_synonyms=input_key_synonyms,
        )
    