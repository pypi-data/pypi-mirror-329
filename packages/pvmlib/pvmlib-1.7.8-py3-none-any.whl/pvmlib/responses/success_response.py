from pvmlib.schemas.success_schema import ResponseGeneralSchema, ResponseMetaSchema
from typing import Any
from pvmlib.context.request_context import RequestContext
from time import time
from datetime import datetime

class TypeSuccess:
    success = {
        200: "SUCCESS",
        201: "CREATED",
        202: "ACCEPTED",
        204: "NO_CONTENT",
        206: "PARTIAL_CONTENT",
        207: "MULTI_STATUS",
        208: "ALREADY_REPORTED",
        226: "IM_USED"
    }

class SuccessResponse(ResponseGeneralSchema):
    
    def __init__(
            self,
            status_code: int = 200,
            data: Any = {},
            message: str = "Request processed successfully"
        ):
        context = RequestContext()
        start_time = context.get_start_time()
        time_elapsed = time() - start_time if start_time else 0.0
        transaction_id = context.get_tracing_id()

        super().__init__( 
            data=data, 
            meta=ResponseMetaSchema(
                transactionID=transaction_id, 
                status=TypeSuccess.success.get(status_code), 
                statusCode=status_code,
                timestamp=datetime.now().isoformat(),
                message=message,
                time_elapsed=time_elapsed
            )
        )