import logging
from fastapi import APIRouter, Depends
import json
from config.settings import settings
import requests
from services import chat_service

logger = logging.getLogger(__name__)

routes = APIRouter(
    prefix="",
    tags=[""],
    responses={404: {"description": "Not found"}},
)


@routes.get("/")
def read_main():
    return {"msg": "Hello World"}

@routes.get("/api/v1/hello")
def hello():
    logger.warning("Routes included")
    
    return {"Hello": "World"}

@routes.post("/api/v1/update")
async def update(payload: dict):
    
    res = json.dumps(payload, ensure_ascii=False, indent=2)
    
    logger.info("Payload:" + res)
    
    # logger.info('payload.get("message", {}).get("entities", []): ' + str(payload.get("message", {}).get("entities", [])))
    
    
    
    # logger.info('payload.get("message", {}).get("entities", [])[:1]: ' + str(payload.get("message", {}).get("entities", [])[:1]))
    
    if next(iter(payload.get("message", {}).get("entities", [])), {}).get("type", "") == "mention" and "@RedKite_GPT_Bot" in payload.get("message", {}).get("text", "") \
            or  (payload.get("message", {}).get("reply_to_message", {}).get("from", {}).get("is_bot", False) \
                and payload.get("message", {}).get("reply_to_message", {}).get("from", {}).get("username", "") == "RedKite_GPT_Bot"):

        chat_id = payload.get("message", {})["chat"]["id"]
        content = payload.get("message", {})["text"]
        
        
        reply_to_id = payload.get("message", {})["message_id"]
        
        await chat_service.reply_to_chat_message(chat_id, content, reply_to_id)
        
