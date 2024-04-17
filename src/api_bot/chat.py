from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain_community.llms import Bedrock
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts.prompt import PromptTemplate

class Chat:
    _messages = []
    def __init__(
        self,
        system_prompt: str = "You are a helpful AI assistant",
        model_name: str = "anthropic.claude-v2",
        region_name: str = "us-west-2",
    ):
        model = Bedrock(
            credentials_profile_name="bedrock-admin",
            model_id=model_name,
            region_name=region_name,
            callbacks=[StreamingStdOutCallbackHandler()],
        )
        
        template = system_prompt + \
        """
            Current conversation:
            {history}
        
            Human: {input}
            AI Assistant:
        """
        
        prompt = PromptTemplate.from_template(template=template)
        prompt = prompt.partial(ref="{{ref}}", username="{{username}}")
        
        self.conversation = ConversationChain(
            prompt=prompt, 
            llm=model, 
            verbose=True, 
            memory=ConversationBufferMemory(ai_prefix="AI Assistant"),
        )

    def _send_req(self, req):
        resp = self.conversation.predict(input=req)
        return resp
    
    def user_message(self, text: str):
        resp = self._send_req(text)
        return resp
