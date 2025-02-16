from beanie import init_beanie
from pymongo import AsyncMongoClient
from functools import lru_cache
from config.settings import settings
import logging

logger = logging.getLogger(__name__)

from config.settings import BackendConfig
settings:BackendConfig = BackendConfig()

class MongoClient:
    def __init__(self):
        self._client = AsyncMongoClient(
            "mongodb://{username}:{password}@{host}:{port}".format(
                username=settings.MONGO_USERNAME,
                password=settings.MONGO_PASSWORD,
                host=settings.MONGO_HOST,
                port=settings.MONGO_PORT,
            ),
            maxPoolSize=100,
            minPoolSize=10,
        )
        
    async def init(self):
        await init_beanie(database=self._client[settings.MONGO_DB], document_models=[
            # Add your models here
        ])
    
mongo_client: MongoClient = MongoClient()

@lru_cache()
def get_mongo_client() -> MongoClient:
    return mongo_client

async def init_mongo():
    global mongo_client
    await mongo_client.init()
    logger.info("Mongo client initialized")
    