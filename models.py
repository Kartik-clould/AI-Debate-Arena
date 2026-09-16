from pydantic import BaseModel

class DebateRequest(BaseModel):
    topic:str