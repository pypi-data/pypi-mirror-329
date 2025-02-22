from pydantic import BaseModel

class ResponseMetaSchema(BaseModel):
    transactionID: str
    status: str
    statusCode: int
    timestamp: str
    message: str
    time_elapsed: float