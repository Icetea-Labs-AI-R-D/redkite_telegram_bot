from fastapi.testclient import TestClient
import asyncio
import motor.motor_asyncio
from beanie import init_beanie
from config.settings import settings
from .main import app
from models.documents import ConversationDocument
from pymongo import AsyncMongoClient
import logging

logger = logging.getLogger(__name__)
client = TestClient(app)

async def init_db():
    _client = AsyncMongoClient(
            "mongodb://{username}:{password}@{host}:{port}".format(
                username=settings.MONGO_USERNAME,
                password=settings.MONGO_PASSWORD,
                host=settings.MONGO_HOST,
                port=settings.MONGO_PORT,
            ),
            maxPoolSize=100,
            minPoolSize=10,
        )
    # client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://localhost:27017")
    await init_beanie(database=_client.db_name, document_models=[ConversationDocument])

# Initialize DB before tests
asyncio.run(init_db())




def test_read_main():
    response = client.get("/")
    
    logger.info("Response status code: " + str(response.status_code))
    logger.info("Response: " + str(response.json()))
    
    assert response.status_code == 200
    # assert response.json() == {"msg": "Hello World"}
    
def test_update():
    payload = {
        "update_id": 671917469,
        "message": {
            "message_id": 49,
            "from": {
                "id": 6011081140,
                "is_bot": False,
                "first_name": "Minh",
                "last_name": "Nguyễn Đăng",
                "username": "minhdunk",
                "language_code": "en"
            },
            "chat": {
                "id": -4604596871,
                "title": "Test Bot RedKite",
                "type": "group",
                "all_members_are_administrators": True
            },
            "date": 1739689320,
            "text": "@RedKite_GPT_Bot alo",
            "entities": [
                {
                    "offset": 0,
                    "length": 16,
                    "type": "mention"
                }
            ]
        }
    }
    
    response = client.post("/api/v1/update", json=payload)
    
    logger.info("Response status code: " + str(response.status_code))
    logger.info("Response: " + str(response.json()))
    
    assert response.status_code == 200
    # assert response.json() == {"msg": "Hello World"}