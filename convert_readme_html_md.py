# Python
from html_to_markdown import convert

with open("README.html", "r", encoding="utf-8") as f:
    html_content = f.read()

result = convert(html_content)
print(result.content)        # # Hello\n\nWorld
print(result.metadata)       # title, links, headings, …


with open("README.md", "w", encoding="utf-8") as f:
    f.write(result.content)