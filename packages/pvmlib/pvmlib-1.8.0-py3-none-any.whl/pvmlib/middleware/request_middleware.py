from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from pvmlib.context import RequestContext
import time
import uuid

class TracingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        tracing_id = request.headers.get("transaction_id", str(uuid.uuid4()))
        user_id = request.headers.get("user_id", "anonymous")
        session_id = request.headers.get("session_id", str(uuid.uuid4()))
        client_ip = request.client.host
        user_agent = request.headers.get("user-agent", "unknown")
        request_path = request.url.path
        context = RequestContext()
        context.set_start_time(start_time)
        context.set_tracing_id(tracing_id)
        context.set_user_id(user_id)
        context.set_session_id(session_id)
        context.set_client_ip(client_ip)
        context.set_user_agent(user_agent)
        context.set_request_path(request_path)
        response = await call_next(request)
        return response