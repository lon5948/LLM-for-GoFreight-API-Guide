import json
import os

from api_bot.openapi_parser import OpenApiParser, OpenApiParts
from api_bot.chat import Chat
from api_bot.engine import ProcessingEngine
from api_bot.operation_ids_chat import OperationIdChat

class Agent():
    operation_id_chat: OperationIdChat
    chat: Chat
    engine: ProcessingEngine

    def __init__(self, base_url: str, gf_api_key: str, openapi_json: dict, model_name: str):
        self.base_url = base_url
        self.gf_api_key = gf_api_key
        self.model_name = model_name
        self.openapi_json = openapi_json

    def start(self):
        openapi = self.openapi_json
        openapi_parts, self.openapi_info, self.openapi_request, self.openapi_response = OpenApiParser(openapi).parse()

        stage1_prompt = self.get_stage1_prompt(openapi_parts)
        operation_id_chat = OperationIdChat(template=stage1_prompt)
        
        self.engine1 = ProcessingEngine(chat=operation_id_chat)
    
    def start_next_stage(self, stage2_prompt: str) -> None:
        chat = Chat(template=stage2_prompt)
        self.engine2 = ProcessingEngine(chat=chat)

    def get_stage1_prompt(self, openapi_parts: OpenApiParts) -> str:
        method_definitions = openapi_parts.method_definitions.to_csv()

        stage1_prompt = ""
        dirname = os.path.dirname(__file__)
        with open(dirname + "/../prompt/stage1_prompt.txt", "r") as f:
            stage1_prompt = f.read()

        stage1_prompt = stage1_prompt.format(
            method_definitions = method_definitions
        )
        return stage1_prompt
    
    def get_stage2_prompt(self) -> str:
        stage2_prompt = ""
        dirname = os.path.dirname(__file__)
        with open(dirname + "/../prompt/stage2_prompt.txt", "r") as f:
            stage2_prompt = f.read()
            
        stage2_prompt = stage2_prompt.format(
            base_url = self.base_url,
            gf_api_key = self.gf_api_key
        )
        return stage2_prompt
    
    def ask(self, question):
        ret: dict = self.engine1.ask(question)
        if 'operation_ids' not in ret:
            return "Sorry, can you please provide more information?"
        
        stage2_prompt = self.get_stage2_prompt() 
        self.start_next_stage(stage2_prompt)
        
        responses = ""
        for order, op_id in enumerate(ret['operation_ids']):
            
            if op_id in self.openapi_info:
                info = self.openapi_info[op_id]
                path = f'path: {info["path"]}\n' 
                method = f'method: {info["method"]}\n'
                description = f'description: {info["description"]}\n'
                security = f'security: {info["security"]}\n'
                request = f'request: {self.openapi_request[op_id]}\n'
                response = f'response: {self.openapi_response[op_id]}\n'
            
                inp = "Below is the useful information for the api:\n" + path + method + description + security + request + response
                resp = self.engine2.ask(inp)
                responses += f"Step {order+1}:, {resp}\n\n"
        if responses == "":
           return "Sorry, I don't have the information for your query."
        return responses
