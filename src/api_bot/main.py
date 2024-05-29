import json

from api_bot.chat import Chat
from api_bot.agent import Agent

class ApiSelector:
    chat: Chat

    def __init__(self, base_url: str, gf_api_key: str, openapi_json_path: str, model_name: str):
        self.base_url = base_url
        self.gf_api_key = gf_api_key
        self.openapi_json_path = openapi_json_path
        self.model_name = model_name
    
    def _get_openapi(self) -> dict:
        return self.get_openapi_from_path(self.openapi_json_path)
    
    def get_openapi_from_path(self, path: str):
        with open(path, "r", encoding='utf-8-sig') as f:
            openapi_docs = json.load(f)
        return openapi_docs
    
    def start(self):
        openapi = self._get_openapi()
        engine = Agent(base_url=self.base_url, gf_api_key=self.gf_api_key, model_name=self.model_name, openapi_json=openapi)
        engine.start()
        self.engine = engine

    def ask_question(self, question):
        return self.engine.ask(question)


def start_api_selector(
        openapi_json: str | None = None,
        base_url: str ="http://0.0.0.0:8000",
        gf_api_key: str = "",
        model_name: str = "anthropic.claude-3-sonnet-20240229-v1:0"
    ) -> callable:

    api_selector = ApiSelector(base_url=base_url, gf_api_key=gf_api_key, openapi_json_path=openapi_json, model_name=model_name)
    api_selector.start()
    ask_question = api_selector.ask_question

    while True:
        inp = input(">>> ")
        if inp == "exit": 
            break
        print(ask_question(inp))
