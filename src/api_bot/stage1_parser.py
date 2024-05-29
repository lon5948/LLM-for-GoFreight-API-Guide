from langchain_core.pydantic_v1 import BaseModel, Field

class OperationIds(BaseModel):
    status: str = Field(description="status of the query")
    operation_ids: list = Field(description="operation ids for the query")
