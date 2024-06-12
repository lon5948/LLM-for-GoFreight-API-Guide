from langchain_core.pydantic_v1 import BaseModel, Field

class Instructions(BaseModel):
    status: str = Field(description="status of the query")
    endpoint: str = Field(description="endpoint of the api")
    description: str = Field(description="description of the api")
    curl_commmand: str = Field(description="command to run the api")
    expected_response: str = Field(description="response of the api")
    