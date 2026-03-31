import copy
import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def _normalize_schema(schema: dict) -> dict:
    """Adapts a JSON schema for Groq strict mode:
    - additionalProperties: false on all objects
    - required must list every property key
    """
    schema = copy.deepcopy(schema)
    _normalize_inplace(schema)
    return schema


def _normalize_inplace(node: dict) -> None:
    if not isinstance(node, dict):
        return
    if node.get("type") == "object":
        node["additionalProperties"] = False
        props = node.get("properties", {})
        node["required"] = list(props.keys())
        for prop in props.values():
            _normalize_inplace(prop)
    elif node.get("type") == "array":
        _normalize_inplace(node.get("items", {}))
    elif isinstance(node.get("type"), str) and node["type"] != "null":
        # Allow null so the model can output null when a field is absent on a page
        node["type"] = [node["type"], "null"]


def send_request(prompt: str, schema: dict) -> str:
    schema_for_api = _normalize_schema(schema)
    response = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[{"role": "user", "content": prompt}],
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "extraction",
                "strict": True,
                "schema": schema_for_api,
            },
        },
    )
    return response.choices[0].message.content
