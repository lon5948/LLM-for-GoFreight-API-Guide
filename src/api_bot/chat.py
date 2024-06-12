from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain_aws import ChatBedrock
from langchain.prompts.prompt import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser

from api_bot.stage2_parser import Instructions
class Chat:
    _messages = []
    def __init__(
        self,
        template: str = "You are a helpful AI assistant",
        model_name: str = "anthropic.claude-3-sonnet-20240229-v1:0",
        region_name: str = "us-west-2",
    ):
        model = ChatBedrock(
            credentials_profile_name="bedrock-admin",
            model_id=model_name,
            region_name=region_name,
            callbacks=[StreamingStdOutCallbackHandler()],
        )
        
        template = template + \
        """
            Human: {input}
            AI Assistant:
        """
        
        parser = JsonOutputParser(pydantic_object=Instructions)
        
        prompt = PromptTemplate(
            template=template,
            input_variables=["input"],
        )
        
        self.chain = prompt | model | parser

    def _send_req(self, req):
        resp = self.chain.invoke({"input": req})
        return resp
    
    def user_message(self, text: str):
        resp = self._send_req(text)
        return resp
