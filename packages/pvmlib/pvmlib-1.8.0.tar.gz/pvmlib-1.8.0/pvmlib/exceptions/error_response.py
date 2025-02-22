from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.status import (
    HTTP_422_UNPROCESSABLE_ENTITY,
    HTTP_405_METHOD_NOT_ALLOWED,
    HTTP_500_INTERNAL_SERVER_ERROR,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND
)
from pvmlib.responses.error_response import ErrorResponseException
from pvmlib.utils import Utils
from pvmlib.logs import LoggerSingleton, LogType
import json

EVENT_TYPES = {
    HTTP_500_INTERNAL_SERVER_ERROR: "SERVER_ERROR",
    HTTP_422_UNPROCESSABLE_ENTITY: "VALIDATION_ERROR",
    HTTP_404_NOT_FOUND: "NOT_FOUND",
    HTTP_405_METHOD_NOT_ALLOWED: "METHOD_NOT_ALLOWED",
    HTTP_400_BAD_REQUEST: "BAD_REQUEST",
    ErrorResponseException: "ERROR_RESPONSE"
}

class ExceptionHandlers:
    def __init__(self):
        self.log = LoggerSingleton().logger

    async def internal_server_error_exception_handler(self, request: Request, exc: Exception):
        error_message, error_info = await Utils.get_instance_exception(exc)
        response = ErrorResponseException(
            message=error_message,
            status_code=HTTP_500_INTERNAL_SERVER_ERROR
        )

        self.log.error(
            message=error_info,
            exc_info=exc,
            caller_self=self,
            logType=LogType.INTERNAL,
            event_type=EVENT_TYPES[HTTP_500_INTERNAL_SERVER_ERROR],
            status=str(HTTP_500_INTERNAL_SERVER_ERROR)
        )

        return JSONResponse(content=json.loads(response.detail), status_code=HTTP_500_INTERNAL_SERVER_ERROR)

    async def validation_exception_handler(self, request: Request, exc: RequestValidationError): 
        error_details = Utils.get_error_details(exc.errors())
        error_message = "Validation error: " + ", ".join(error_details)
        response = ErrorResponseException(
            message=error_message,
            status_code=HTTP_422_UNPROCESSABLE_ENTITY
        )

        additional_info = {
            "url": str(request.url),
            "endpoint": request.scope.get("endpoint").__name__ if request.scope.get("endpoint") else None
        }

        self.log.warning(
            message=error_message,
            exc_info=exc,
            caller_self=self,
            logType=LogType.SYSTEM,
            event_type=EVENT_TYPES[HTTP_422_UNPROCESSABLE_ENTITY],
            destination_ip=request.client.host,
            additional_info=additional_info,
            status=str(HTTP_422_UNPROCESSABLE_ENTITY)
        )

        return JSONResponse(content=json.loads(response.detail), status_code=HTTP_422_UNPROCESSABLE_ENTITY)

    async def not_found_exception_handler(self, request: Request, exc: HTTPException):
        error_message = "Resource not found"
        response = ErrorResponseException(
            message=error_message,
            status_code=HTTP_404_NOT_FOUND
        )

        additional_info = {
            "url": str(request.url),
            "endpoint": request.scope.get("endpoint").__name__ if request.scope.get("endpoint") else None
        }

        self.log.warning(
            message=error_message,
            exc_info=exc,
            caller_self=self,
            logType=LogType.SYSTEM,
            event_type=EVENT_TYPES[HTTP_404_NOT_FOUND],
            destination_ip=request.client.host,
            additional_info=additional_info,
            status=str(exc.status_code)
        )

        return JSONResponse(content=json.loads(response.detail), status_code=exc.status_code) 

    async def method_not_allowed_exception_handler(self, request: Request, exc: HTTPException):   
        error_message = "Method not allowed."
        response = ErrorResponseException(
            message=error_message,
            status_code=HTTP_405_METHOD_NOT_ALLOWED
        )

        self.log.warning(
            message=error_message,
            exc_info=exc,
            caller_self=self,
            logType=LogType.SYSTEM,
            event_type=EVENT_TYPES[HTTP_405_METHOD_NOT_ALLOWED],
            status=str(exc.status_code)
        )

        return JSONResponse(content=json.loads(response.detail), status_code=exc.status_code)

    async def bad_request_exception_handler(self, request: Request, exc: HTTPException):
        error_message = "Bad request."
        response = ErrorResponseException(
            message=error_message,
            status_code=HTTP_400_BAD_REQUEST
        )

        self.log.warning(
            message=error_message,
            exc_info=exc,
            caller_self=self,
            logType=LogType.SYSTEM,
            event_type=EVENT_TYPES[HTTP_400_BAD_REQUEST],
            status=str(exc.status_code)
        )

        return JSONResponse(content=json.loads(response.detail), status_code=exc.status_code)

    async def error_exception_handler(self, request: Request, exc: ErrorResponseException):
        return JSONResponse(content=json.loads(exc.detail), status_code=exc.status_code)

def register_exception_handlers(app: FastAPI):
    handlers = ExceptionHandlers()
    app.add_exception_handler(HTTP_500_INTERNAL_SERVER_ERROR, handlers.internal_server_error_exception_handler)
    app.add_exception_handler(RequestValidationError, handlers.validation_exception_handler)
    app.add_exception_handler(HTTP_404_NOT_FOUND, handlers.not_found_exception_handler)
    app.add_exception_handler(HTTP_405_METHOD_NOT_ALLOWED, handlers.method_not_allowed_exception_handler)
    app.add_exception_handler(HTTP_400_BAD_REQUEST, handlers.bad_request_exception_handler)
    app.add_exception_handler(ErrorResponseException, handlers.error_exception_handler)