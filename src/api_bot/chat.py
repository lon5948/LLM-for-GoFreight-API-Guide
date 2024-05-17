from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain_community.llms import Bedrock
from langchain.prompts.prompt import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

class Chat:
    _messages = []
    def __init__(
        self,
        template: str = "You are a helpful AI assistant",
        model_name: str = "anthropic.claude-v2",
        region_name: str = "us-west-2",
    ):
        model = Bedrock(
            credentials_profile_name="bedrock-admin",
            model_id=model_name,
            region_name=region_name,
            callbacks=[StreamingStdOutCallbackHandler()],
        )
        
        with open("example_prompt.txt", "w") as f:
            f.write(template)
        
        template = template + \
        """
            Human: {input}
            AI Assistant:
        """
        
        parser = StrOutputParser()
        
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
