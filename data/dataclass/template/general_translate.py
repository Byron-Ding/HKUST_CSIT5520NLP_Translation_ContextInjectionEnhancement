import dataclasses
from typing import Final

@dataclasses.dataclass(frozen=True)
class GeneralTemplate:
    english_synonyms_dictionary_url: Final[str] = r"https://www.collinsdictionary.com/dictionary/english-thesaurus/{word}"
    translate_template: Final[str] = r"""
{input_key_synonyms}
//////////////////////////////////////////////

Input-Output-Task: Translate
Input: {input_text}
Input-language: {input_language}
Output-language: {output_language}
Output:

//////////////////////////////////////////////
Rules:
1. Allow optional comments, after Each word;
    comments should |point out>  the key characteristic, especially the original meaning |of> each word.
Output format:
Note: each "(comment)" |is> optional
    Format is: 
    <output>input language (translation and output language comment)</output>
    <output_without_comment>translation without comment</output_without_comment>
    example:
    "<output>ori-word1 (word1-comment) ori-word2 (word2-comment) ori-word3 (word3-comment)..... ori-ordN (wordN-comment)</output>
    <output_without_comment>word1 word2 word3..... wordN</output_without_comment>
    " 
Note: Only allow one output.
Note: Comment |are> in Output-Language, in {output_language}
Note: the output comment is used to distinguish original meaning from other synonyms
3. Compare the similar word of each word -> |point out> the key characteristic |of> each word
4. Characteristic |based on> the original meaning; optional for evolute to the extension |of> each word;
    original meaning |is> important.
5. |Annotate> the original meaning in the comment, which shown |as/in> the output language
6. Use <output> </output> to wrap the output_translation_with_comment, which should be in the output language
"""
    
    translate_template_baseline: Final[str] = r"""
Input-Output-Task: Translate
Input: {input_text}
Input-language: {input_language}
Output-language: {output_language}
Output:
"""
    
    translate_template_without_synonyms: Final[str] = r"""
//////////////////////////////////////////////

Input-Output-Task: Translate
Input: {input_text}
Input-language: {input_language}
Output-language: {output_language}
Output:

//////////////////////////////////////////////
Rules:
1. Allow optional comments, after Each word;
    comments should |point out>  the key characteristic, especially the original meaning |of> each word.
Output format:
Note: each "(comment)" |is> optional
    Format is: 
    <output>input language (translation and output language comment)</output>
    <output_without_comment>translation without comment</output_without_comment>
    example:
    "<output>ori-word1 (word1-comment) ori-word2 (word2-comment) ori-word3 (word3-comment)..... ori-ordN (wordN-comment)</output>
    <output_without_comment>word1 word2 word3..... wordN</output_without_comment>
    " 
Note: Only allow one output.
Note: Comment |are> in Output-Language, in {output_language}
Note: the output comment is used to distinguish original meaning from other synonyms
3. Compare the similar word of each word -> |point out> the key characteristic |of> each word
4. Characteristic |based on> the original meaning; optional for evolute to the extension |of> each word;
    original meaning |is> important.
5. |Annotate> the original meaning in the comment, which shown |as/in> the output language
6. Use <output> </output> to wrap the output_translation_with_comment, which should be in the output language
"""
    translate_template_with_synonyms_but_no_rules: Final[str] = r"""{input_key_synonyms}
//////////////////////////////////////////////

Input-Output-Task: Translate
Input: {input_text}
Input-language: {input_language}
Output-language: {output_language}
Output:
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
    
    
    @staticmethod
    def format_translate_template_baseline(
        input_text: str,
        input_language: str,
        output_language: str,
    ) -> str:
        return GeneralTemplate.translate_template_baseline.format(
            input_text=input_text,
            input_language=input_language,
            output_language=output_language,
        )
        
        
    @staticmethod
    def format_translate_template_without_synonyms(
        input_text: str,
        input_language: str,
        output_language: str,
    ) -> str:
        return GeneralTemplate.translate_template_without_synonyms.format(
            input_text=input_text,
            input_language=input_language,
            output_language=output_language,
        )
        
        
    @staticmethod
    def format_translate_template_with_synonyms_but_no_rules(
        input_text: str,
        input_language: str,
        output_language: str,
        input_key_synonyms: str,
    ) -> str:
        return GeneralTemplate.translate_template_with_synonyms_but_no_rules.format(
            input_text=input_text,
            input_language=input_language,
            output_language=output_language,
            input_key_synonyms=input_key_synonyms,
        )
        
        