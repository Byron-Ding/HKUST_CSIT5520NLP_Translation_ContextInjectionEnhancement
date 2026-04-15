template: str = '''
import translate
result: string = translate.translate(
    "en",
    "zh-CN",
    "The meeting is critical for the success of the project."
)
print(result)
'''

# 利用多头注意力的机制
# 1. 分隔符
# ∵ Q = XWq, K = XWk, V = XWv
# Attention(Q, K, V) = softmax(QK^T / sqrt(d_k))V
# Result = Attention(Q, K, V)
#        = softmax((XWq)(XWk)^T / sqrt(d_k))XWv
#        = softmax(XWqWk^TX^T / sqrt(d_k))XWv
# 在训练好的模型里，通常相似的输入（比如语义接近的词）会让 Q 和 K 的点积更大，从而在 softmax 里得到更高的注意力权重。
# 
# ∴ 要增强某个位置，需要与其他地方提高相似度
template: str = '''
------------------------------------------------------------------
Task: Translate:
Original: "The meeting is critical for the success of the project."
Original-language: en-us
Target-language: zh-cn
Output:

------------------------------------------------------------------
https://www.collinsdictionary.com/dictionary/english-thesaurus/the
https://www.collinsdictionary.com/dictionary/english-thesaurus/project
https://www.collinsdictionary.com/dictionary/english-thesaurus/is
https://www.collinsdictionary.com/dictionary/english-thesaurus/vital
Rules:
1. Allow optional comments, after each word, format like:  word (comment), enhanced characteristic of this word
2. "The (comment) project is (comment)....." in chinese
3. Compare the synonyms and point out the key characteristic
4. Show the exact original meaning as comment enhancement
5. Consider where each unit's meaning extended from is original meaning
6. Annotate in the translated comment
------------------------------------------------------------------
output result
'''
import lmstudio as lms
import pathlib

lmstudio_root_path: pathlib.Path = pathlib.Path(r"F:/.lmstudio/lmstudio-community/")

meta_llama_path: str = r"meta-llama-3.1-8b-instruct"
qwen_path: str = r"qwen/qwen3.5-9b"

model = lms.llm(
    qwen_path,
)
result = model.respond(template)

print(result)