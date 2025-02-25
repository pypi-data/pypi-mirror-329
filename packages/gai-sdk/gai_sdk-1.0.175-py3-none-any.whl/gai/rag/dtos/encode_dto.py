from pydantic import BaseModel

class EncodeRequest(BaseModel):
    text: str  # Text to encode

class EncodeResponse(BaseModel):
    encoded_data: list[float]  # The result of the encoding process