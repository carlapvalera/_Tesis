import openai
from pydantic import BaseModel, Field
from fireworks.client import Fireworks

class LLM():
    def __init__(self, api_key: str = "fw_3ZXb6WWaLuUNnJZnvXWTwEY2", model: str = "accounts/fireworks/models/llama-v3p1-8b-instruct") -> None:
        self.__SEND_GLOBAL_STATEMENT = True
        self.__api_key = api_key
        self.__model = model
        self.__global_statements = []

        self.__client = Fireworks(api_key=self.__api_key)

client = openai.OpenAI(
    base_url="https://api.fireworks.ai/inference/v1",
    api_key="fw_3Zf7HrTqgxNgJFhWovNoxZcZ",
)

class Result(BaseModel):
    winner: str

chat_completion = client.chat.completions.create(
    model="accounts/fireworks/models/llama-v3p1-8b-instruct",
    response_format={"type": "json_object", "schema": Result.model_json_schema()},
    messages=[
        {
            "role": "user",
            "content": "Who won the US presidential election in 2012? Reply just in one JSON.",
        },
    ],
)

print(repr(chat_completion.choices[0].message.content))

'{\n "winner": "Barack Obama"\n}'
