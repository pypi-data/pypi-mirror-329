import time
import json
import re
from pydantic import BaseModel
from langchain_core.output_parsers import JsonOutputParser

def get_current_time():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())

def get_schema_dict_from_pydanticmodel(model: BaseModel) -> dict:
    return model.model_dump()

def dict_to_json_file(data: dict, file_path: str):
    with open(file_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)


def extract_json_from_llama_like_llms(text):
    pattern = r'```json\n(.*?)\n```'
    match = re.search(pattern, text, re.DOTALL)
    if match:
        json_str = match.group(1)
        return json.loads(json_str)
    raise ValueError("No JSON content found between ```json``` markers")

   

class JsonOutputParserWithPostProcessing(JsonOutputParser):
    def parse(self, text):
        # Extract JSON from text that might contain thinking tags
        parts = text.split("</think>\n\n", 1)
        json_str = parts[1] if len(parts) > 1 else text
        
        # Fix trailing commas
        json_str = re.sub(r',\s*}', '}', json_str)
        
        # Parse the cleaned JSON
        return super().parse(json_str)

    