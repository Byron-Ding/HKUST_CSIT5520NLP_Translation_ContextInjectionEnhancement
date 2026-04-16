import similarities 
import pathlib

# data path
project_root_path = pathlib.Path(__file__).parent.parent
data_path = project_root_path / "output" / "qwen" / "qwen3.5-9b"
print(data_path)