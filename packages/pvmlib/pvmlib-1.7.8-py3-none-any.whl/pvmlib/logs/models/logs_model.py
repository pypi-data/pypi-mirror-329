from typing import Any, Dict, Optional
from pydantic import BaseModel

class Application(BaseModel):
    name: str
    version: str
    env: str
    kind: str

class Measurement(BaseModel):
    method: str
    elapsedTime: float

class ExceptionModel(BaseModel):
    name: str
    message: str
    stackTrace: str

class DataLogger(BaseModel):
    level: str
    schemaVersion: str
    logType: str
    sourceIP: str
    status: str
    message: str
    logOrigin: str
    timestamp: str
    tracingId: str
    hostname: str
    eventType: str
    application: Application
    measurement: Measurement
    destinationIP: str
    additionalInfo: Optional[Dict[str, Any]] = None
    exception: Optional[ExceptionModel] = None
    sourceFile: str = None
