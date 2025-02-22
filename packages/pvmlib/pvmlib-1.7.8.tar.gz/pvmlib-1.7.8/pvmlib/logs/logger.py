import os
import logging
import socket
import inspect
import traceback
import uuid
from time import time
from typing import Optional, Any, Union
from colorama import Fore, Style, init
from datetime import datetime
from pvmlib.logs.models import Application, Measurement, DataLogger, ExceptionModel
from pvmlib.logs.utils import LogType, LogLevelColors
from pvmlib.context.request_context import RequestContext
from pvmlib.patterns.decorator import sensitive_info_decorator

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

logging.basicConfig(format='%(levelname)s: %(asctime)s - %(message)s', datefmt=DATE_FORMAT)
logger = logging.getLogger("uvicorn")

init(autoreset=True)
class LogData:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(LogData, cls).__new__(cls)
            cls._instance.__initialize(*args, **kwargs)
        return cls._instance

    def __initialize(self, origin: str = "INTERNAL"):
        self.logger = logger
        self.schema_version = os.getenv("VERSION_LOG", "1.0.0")
        self.log_origin = origin
        self.tracing_id = "N/A"
        self.hostname = socket.gethostname()
        self.appname = os.getenv("APP_NAME", )
        self.source_ip = socket.gethostbyname(socket.gethostname())
        self.destination_ip = "N/A"
        self.additional_info = {}
        self.app = Application(
            name=os.getenv("APP_NAME", "default"),
            version=os.getenv("API_VERSION", "default"),
            env=os.getenv("ENV", "default"),
            kind=os.getenv("APP_KIND", "default"))
        self.initialized = True

    @sensitive_info_decorator
    def log(
            self, 
            level: int, 
            message: str, 
            logType: str = LogType.INTERNAL, 
            event_type: str = "EVENT", 
            status: str = "SUCCESS", 
            destination_ip: str = None,
            additional_info: Optional[dict] = None,
            exc_info: Union[None, Exception, tuple] = None,
            caller_self: Optional[Any] = None
        ) -> None:
        context = RequestContext()
        
        if destination_ip is not None:
            self.destination_ip = destination_ip
        
        if caller_self is not None:
            method_name = caller_self.__class__.__name__
        else:
            caller_frame = inspect.stack()[2]
            method_name = caller_frame.function

        exception_model = None
        source_file = "N/A"

        if exc_info:
            if isinstance(exc_info, tuple) and len(exc_info) == 3:
                exc_type, exc_value, exc_tb = exc_info
            elif isinstance(exc_info, Exception):
                exc_type, exc_value, exc_tb = type(exc_info), exc_info, exc_info.__traceback__
            else:
                exc_type, exc_value, exc_tb = None, None, None

            if exc_type and exc_value and exc_tb:
                stack_trace = traceback.format_exception(exc_type, exc_value, exc_tb)
                exception_model = ExceptionModel(
                    name=exc_type.__name__,
                    message=str(exc_value),
                    stackTrace=' '.join(stack_trace)
                )
                if additional_info is None:
                    additional_info = {}

                tb = traceback.extract_tb(exc_tb)
                if tb:
                    source_file_trace = tb[-1].filename
                source_file = source_file_trace
        
        log_entry = DataLogger(
            level=logging.getLevelName(level),
            schemaVersion=self.schema_version,
            logType=logType,
            sourceIP=self.source_ip,
            status=status,
            message=message,
            logOrigin=self.log_origin,
            timestamp=datetime.now().strftime(DATE_FORMAT),
            tracingId=context.get_tracing_id(),
            hostname=self.hostname,
            eventType=f"{logType}_{event_type.upper()}",
            application=self.app,
            measurement=Measurement(
                method=method_name,
                elapsedTime=time() - context.get_start_time() if context.get_start_time() else 0,
                status=status,
            ),
            destinationIP=self.destination_ip,
            additionalInfo=additional_info or self.additional_info,
            exception=exception_model,
            sourceFile=source_file
        )

        colored_date = f"{Fore.CYAN}{log_entry.timestamp}{Style.RESET_ALL}"
        colored_name = f"{Fore.CYAN}{self.appname}{Style.RESET_ALL}"
        color_status = getattr(LogLevelColors, log_entry.level, Fore.WHITE) + log_entry.status + Style.RESET_ALL

        log_message = f'{colored_date} - {colored_name} - {log_entry.model_dump()} - Status: {color_status}'
        self.logger.log(level, log_message)

    def info(
            self, 
            message: str, 
            logType: str = LogType.SYSTEM, 
            event_type: str = "EVENT", 
            status: str = "SUCCESS", 
            destination_ip: str = None,
            additional_info: dict = None,
            caller_self: Optional[Any] = None
        ):
        self.log(
            logging.INFO, 
            message, 
            logType, 
            event_type, 
            status, 
            destination_ip,
            additional_info,
            caller_self
        )

    def error(
            self, 
            message: str, 
            logType: str = LogType.SYSTEM, 
            event_type: str = "EVENT", 
            status: str = "ERROR", 
            destination_ip: str = None,
            additional_info: dict = None,
            exc_info: Optional[Exception] = None,
            caller_self: Optional[Any] = None
        ):
        self.log(
            logging.ERROR, 
            message, 
            logType, 
            event_type, 
            status, 
            destination_ip,
            additional_info,
            exc_info,
            caller_self
        )

    def warning(
            self, 
            message: str, 
            logType: str = LogType.SYSTEM, 
            event_type: str = "EVENT", 
            status: str = "WARNING", 
            destination_ip: str = None,
            additional_info: dict = None,
            exc_info: Optional[Exception] = None,
            caller_self: Optional[Any] = None
            ):
        self.log(
            logging.WARNING, 
            message, 
            logType, 
            event_type, 
            status, 
            destination_ip,
            additional_info,
            exc_info,
            caller_self
            )

    def debug(
            self, 
            message: str, 
            logType: str = LogType.SYSTEM, 
            event_type: str = "EVENT", 
            status: str = "DEBUG", 
            destination_ip: str = None,
            additional_info: dict = None,
            exc_info: Optional[Exception] = None,
            caller_self: Optional[Any] = None
            ):
        self.log(
            logging.DEBUG, 
            message, 
            logType, 
            event_type, 
            status, 
            destination_ip, 
            additional_info,
            exc_info,
            caller_self
            )

    def critical(
            self, 
            message: str, 
            logType: str = LogType.SYSTEM, 
            event_type: str = "EVENT", 
            status: str = "CRITICAL", 
            destination_ip: str = None,
            additional_info: dict = None,
            exc_info: Optional[Exception] = None,
            caller_self: Optional[Any] = None
            ):
        self.log(
            logging.CRITICAL, 
            message, 
            logType, 
            event_type, 
            status, 
            destination_ip,
            additional_info,
            exc_info,
            caller_self
            )

class LoggerSingleton:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(LoggerSingleton, cls).__new__(cls)
            cls._instance.__initialize(*args, **kwargs)
            cls._instance._id = str(uuid.uuid4())
        return cls._instance
            
    def __initialize(self, *args, **kwargs):
        self.logger = LogData()
    
    def get_instance_id(self):
        return self._id