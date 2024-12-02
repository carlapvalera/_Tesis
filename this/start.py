
from fireworks.client import Fireworks
import re

class LLM():
    def __init__(self, api_key: str = "fw_3ZXb6WWaLuUNnJZnvXWTwEY2", model: str = "accounts/fireworks/models/llama-v3p1-8b-instruct") -> None:
        self.__SEND_GLOBAL_STATEMENT = True
        self.__api_key = api_key
        self.__model = model
        self.__global_statements = []

        self.__client = Fireworks(api_key=self.__api_key)

# TODO: Fill get_context and save_context with the back-end like part with the RAG and BERT components
    def _get_context(self,query):
        return ""
    def _save_context(self,answer):
        pass
    
    def _send(self, query, content=""):
        response = self.__client.chat.completions.create(
            model=self.__model,
            response_format={"type": "json_object", "schema": Result.model_json_schema()},
            messages=[
                {
                    "role": "user",
                    "content": (
                        "\n".join(self.__global_statements) if self.__SEND_GLOBAL_STATEMENT else ""
                    )
                    + content
                    + "\n"
                    + query,
                }
            ],
        )
        self.__SEND_GLOBAL_STATEMENT = True
        return response.choices[0].message.content
    
    def _extract_global_statement(self, query):
        message = f'Identify the exact part of the following text that represents a statement changing the conversation type. Enclose it within square brackets. If no such statement exists, return []. Text: "{query}"'
        answer = self._send(query=message)
        # Attempt to extract from AI response first
        match = re.search(r"\[(.*?)\]", answer)
        if match:
            extracted_content = match.group(1).strip()
            if extracted_content:
                self.__global_statements.append(extracted_content)
                self.__SEND_GLOBAL_STATEMENT = False
                return
        # If AI fails, fall back to regex for potential patterns
        match = re.search(
            r"(from now on|talk to me like|pretend you are).*(?=[.?!])",
            query,
            re.IGNORECASE,
        )
        if match:
            extracted_content = match.group(0).strip()
            self.__global_statements.append(extracted_content)
            self.__SEND_GLOBAL_STATEMENT = False
    def _resolve_conflict_with_global_statements(self):
        if len(self.__global_statements) > 1:
            message = f'Identify the statements that can contradict themselfs and just left the last ones. Enclose the final result within square brackets. If no such statement exists, return []. Text: "{"\n".join(self.__global_statements)}"'
            answer = self._send(query=message)
            match = re.search(r"\[(.*?)\]", answer)
            if match:
                extracted_content = match.group(1).strip()
                if extracted_content:
                    self.__global_statements = [extracted_content]
                    return
        else:
            return
        
    def send_query(self, query) -> str:
            self._extract_global_statement(query)
            self._resolve_conflict_with_global_statements()
            answer = self._send(query, self._get_context(query))
            self._save_context(answer)
            return answer
    
if __name__ == "__main__":
    llm = LLM()
    while True:
        query = input("user: ")
        answer = llm.send_query(query)
        print(answer)