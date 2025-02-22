import abc
import os
from motor.motor_asyncio import AsyncIOMotorClient
from contextlib import contextmanager
from pvmlib.logs.logger import LoggerSingleton

class Session:
    pass

class Database:
    @abc.abstractmethod
    @contextmanager
    def session(self): pass

class DatabaseManager(Database):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(DatabaseManager, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.mongo_database = None
            self.mongo_client = None
            self.initialized = True

    async def connect_to_mongo(self):
        logger = LoggerSingleton().logger
        try:
            mongo_uri = os.getenv("MONGO_URI", "localhost:27017")
            mongo_timeout_ms = os.getenv("MONGO_TIMEOUT_MS", "5000")
            mongo_max_pool_size = os.getenv("MONGO_MAX_POOL_SIZE", "100")
            mongo_db_name = os.getenv("MONGO_DB_NAME")

            if not mongo_uri or not mongo_db_name:
                raise ValueError("MONGO_URI and MONGO_DB_NAME must be set in environment variables")

            self.mongo_client = AsyncIOMotorClient(
                mongo_uri,
                serverSelectionTimeoutMS=int(mongo_timeout_ms),
                maxPoolSize=int(mongo_max_pool_size)
            )
            self.mongo_database = self.mongo_client[mongo_db_name]
        except Exception as e:
            raise

    async def disconnect_from_mongo(self):
        if self.mongo_client:
            self.mongo_client.close()

    @contextmanager
    def session(self):
        try:
            yield self.mongo_database
        finally:
            pass 

database_manager = DatabaseManager()