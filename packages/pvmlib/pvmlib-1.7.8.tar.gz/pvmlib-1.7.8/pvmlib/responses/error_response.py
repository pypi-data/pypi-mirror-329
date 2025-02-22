from fastapi import HTTPException
from pvmlib.schemas.errors_schema import ErrorGeneralSchema
from pvmlib.logs.logger import LoggerSingleton
from pvmlib.context import RequestContext
from pvmlib.schemas import ResponseMetaSchema
import json
from datetime import datetime
import time

log = LoggerSingleton()

class TypeError:
    errors = {
        500: "INTERNAL_SERVER_ERROR",
        400: "BAD_REQUEST",
        401: "UNAUTHORIZED",
        403: "FORBIDDEN",
        404: "NOT_FOUND",
        405: "METHOD_NOT_ALLOWED",
        409: "CONFLICT",
        415: "UNSUPPORTED_MEDIA_TYPE",
        422: "UNPROCESSABLE_ENTITY",
        501: "NOT_IMPLEMENTED",
        503: "SERVICE_UNAVAILABLE",
        504: "GATEWAY_TIMEOUT"
    }

class ErrorResponseException(HTTPException):
    def __init__(
            self,
            message: str = "ERROR",
            status_code: int = 500,
        ):
        context = RequestContext()
        start_time = context.get_start_time()
        time_elapsed = time.time() - start_time if start_time else 0.0
        transaction_id = context.get_tracing_id()

        response = ErrorGeneralSchema(
            data=None,
            meta=ResponseMetaSchema(
                transactionID=transaction_id,
                status=TypeError.errors.get(status_code, "UNKNOWN_ERROR"),
                statusCode=status_code,
                timestamp=datetime.now().isoformat(),
                message=message,
                time_elapsed=time_elapsed
            ).model_dump()
        )

        super().__init__(status_code=status_code, detail=json.dumps(response.model_dump()))