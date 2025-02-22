import threading

class RequestContext:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super(RequestContext, cls).__new__(cls)
                    cls._instance.reset()
        return cls._instance

    def reset(self):
        self.start_time = None
        self.tracing_id = None
        self.user_id = None
        self.session_id = None
        self.client_ip = None
        self.user_agent = None
        self.request_path = None

    def set_start_time(self, start_time):
        self.start_time = start_time

    def get_start_time(self):
        return self.start_time

    def set_tracing_id(self, tracing_id):
        self.tracing_id = tracing_id

    def get_tracing_id(self):
        return self.tracing_id

    def set_user_id(self, user_id):
        self.user_id = user_id

    def get_user_id(self):
        return self.user_id

    def set_session_id(self, session_id):
        self.session_id = session_id

    def get_session_id(self):
        return self.session_id

    def set_client_ip(self, client_ip):
        self.client_ip = client_ip

    def get_client_ip(self):
        return self.client_ip

    def set_user_agent(self, user_agent):
        self.user_agent = user_agent

    def get_user_agent(self):
        return self.user_agent

    def set_request_path(self, request_path):
        self.request_path = request_path

    def get_request_path(self):
        return self.request_path