from pydantic import BaseModel
from typing import Dict

class LivenessResponse(BaseModel):
    status: str
    code: int
    dependencies: Dict[str, str]

class ReadinessResponse(BaseModel):
    status: str
    code: int
    dependencies: Dict[str, str]

responses_liveness = {
    200: {
        "description": "Successful Response",
        "content": {
            "application/json": {
                "schema": {
                    "$ref": "#/components/schemas/LivenessResponse"
                },
                "example": {
                    "status": "UP",
                    "code": 200,
                    "dependencies": {
                        "mongodb": "UP",
                        "auth-service": "UP",
                        "payment-service": "UP",
                        "notification-service": "DOWN"
                    }
                }
            }
        }
    }
}

responses_readiness = {
    200: {
        "description": "Successful Response",
        "content": {
            "application/json": {
                "schema": {
                    "$ref": "#/components/schemas/ReadinessResponse"
                },
                "example": {
                    "status": "ready",
                    "code": 200,
                    "dependencies": {
                        "mongodb": "UP",
                        "auth-service": "UP",
                        "payment-service": "UP",
                        "notification-service": "DOWN"
                    }
                }
            }
        }
    }
}