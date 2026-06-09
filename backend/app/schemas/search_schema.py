from pydantic import BaseModel


class SearchSchema(BaseModel):
    query: str