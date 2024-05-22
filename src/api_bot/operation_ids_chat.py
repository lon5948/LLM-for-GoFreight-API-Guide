from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain_aws import ChatBedrock
from langchain_core.output_parsers import JsonOutputParser
from langchain.prompts.prompt import PromptTemplate

from api_bot.output_parser import OperationIds

class OperationIdChat:
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
            {format_instructions}
            
            Human: {input}
            AI Assistant:
        """
        
        parser = JsonOutputParser(pydantic_object=OperationIds)
        
        prompt = PromptTemplate(
            template=template,
            input_variables=["input"],
            partial_variables={"format_instructions": parser.get_format_instructions(), "ref": "{{ref}}", "username": "{{username}}"},
        )
        
        self.chain = prompt | model | parser

    def _send_req(self, req):
        resp = self.chain.invoke({"input": req})
        return resp
    
    def user_message(self, text: str):
        resp = self._send_req(text)
        return resp
