import logging

from api_bot.chat import Chat

logger = logging.getLogger(__name__)

class ProcessingEngine:
    def __init__(self, chat: Chat):
        self.chat = chat
        
    def ask(self, question) -> str:
        response: str = self.chat.user_message(question)
        return response
