import openai
from pydantic import BaseModel, Field
from fireworks.client import Fireworks

client = openai.OpenAI(
    base_url="https://api.fireworks.ai/inference/v1",
    api_key="fw_3Zf7HrTqgxNgJFhWovNoxZcZ",
)

class Result(BaseModel):
    code : str

chat_completion = client.chat.completions.create(
    model="accounts/fireworks/models/llama-v3p1-8b-instruct",
    response_format={"type": "json_object", "schema": Result.model_json_schema()},
    messages=[
        {
            "role": "user",
            "content": "supon q tengo una tabla de personas y susu eddades dame el codigo a ejecutar q el resultado sea la cantidad de personas mayor de 30",
        },
    ],
)

print(repr(chat_completion.choices[0].message.content))

'{\n "winner": "Barack Obama"\n}'
