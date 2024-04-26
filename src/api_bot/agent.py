import os

from api_bot.openapi_parser import OpenApiParser, OpenApiParts
from api_bot.chat import Chat
from api_bot.engine import ProcessingEngine

class Agent():
    chat: Chat
    engine: ProcessingEngine

    def __init__(self, base_url: str, openapi_json: dict, model_name: str):
        self.base_url = base_url
        self.model_name = model_name
        self.openapi_json = openapi_json

    def start(self):
        openapi = self.openapi_json
        openapi_parts, self.openapi_request, self.openapi_response = OpenApiParser(openapi).parse()

        stage1_prompt = self.get_stage1_prompt(openapi_parts)
        
        chat = Chat(stage1_prompt=stage1_prompt)
        engine = ProcessingEngine(chat=chat, base_url=self.base_url)
        self.chat = chat
        self.engine = engine

    def get_stage1_prompt(self, openapi_parts: OpenApiParts) -> str:
        method_definitions = openapi_parts.method_definitions.to_csv()
        security_definitions = openapi_parts.security_definitions.to_csv()

        stage1_prompt = ""
        dirname = os.path.dirname(__file__)
        with open(dirname + "/../prompt/stage1_prompt.txt", "r") as f:
            stage1_prompt = f.read()

        stage1_prompt = stage1_prompt.format(
            method_definitions = method_definitions,
            security_definitions = security_definitions
        )
        return stage1_prompt
    
    def get_stage2_prompt(self, operation_ids: list) -> str:
        request_and_response_body = []        
        for op_id in operation_ids:
            request = self.openapi_request[op_id]
            response = self.openapi_response[op_id]
            request_and_response_body.append({
                op_id: {
                    "request": request,
                    "response": response
                }
            })

        stage2_prompt = ""
        dirname = os.path.dirname(__file__)
        with open(dirname + "/../prompt/stage2_prompt.txt", "r") as f:
            stage2_prompt = f.read()

        stage2_prompt = stage2_prompt.format(
            request_and_response_body = request_and_response_body
        )
        return stage2_prompt
    
    def ask(self, question):
        inp1 = f"Find Operaton ID from OpenAPI documentation.\nUser Query: {question}"
        operation_id: str = self.engine.ask(inp1)
        
        op_list = operation_id.split(',')
        
        self.get_stage2_prompt(op_list)
        
        inp2 = f"Base URL is {self.base_url} and teach user how to finish user query according to API documentation.\nUser Query: {question}"
        res: str = self.engine.ask(inp2)

        return res
