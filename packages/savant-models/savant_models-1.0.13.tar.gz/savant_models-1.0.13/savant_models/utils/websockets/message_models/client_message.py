from pydantic import BaseModel


class ClientMessage(BaseModel):
    message: str
    connection: bool

