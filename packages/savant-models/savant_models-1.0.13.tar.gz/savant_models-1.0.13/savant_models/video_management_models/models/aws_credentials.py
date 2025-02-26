from pydantic import BaseModel


class AWSCredentials(BaseModel):
    access_key: str
    secret_key: str
    session_token: str
