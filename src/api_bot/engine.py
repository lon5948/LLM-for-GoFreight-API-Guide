import logging

from api_bot.chat import Chat

logger = logging.getLogger(__name__)

class ProcessingEngine:
    def __init__(self, chat: Chat, base_url = "http://0.0.0.0:8000"):
        self.chat = chat
        self.base_url = base_url
        
    def ask(self, question) -> str:
        response: str = self.chat.user_message(question)
        return response
