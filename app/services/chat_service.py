import requests
import json
from config.settings import settings
import logging
from services import mongo_service
# import mongo_service
from typing import Optional
import logging

logger = logging.getLogger(__name__)

TOKEN = settings.TELEGRAM_BOT_TOKEN
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TOKEN}/"

mongo_service = mongo_service.get_mongo_service()

def send_message(chat_id, text, payload):
    """Send a message to a Telegram user."""
    url = TELEGRAM_API_URL + "sendMessage"
    payload = {"chat_id": chat_id, "text": text, "parse_mode": "Markdown" , **payload}
    
    # json_data = json.dumps(payload)
    logger.info(f"Sending message to chat ID {chat_id}: {text}")
    
    res = requests.post(url, json=payload)
    
    if res.status_code != 200:
        logger.error(f"Failed to send message to chat ID {chat_id}: {res.text}")
    else:
        logger.info(f"Message sent to chat ID {chat_id}")
        
    logger.info(f"Response: {res.text}")
    
    return res

def send_chat_message_to_agent(conversation_id: str, content: str, global_topic: dict = None) -> dict:
    """
    Send a chat message to the chatbot API.
    
    Args:
        conversation_id (str): The ID of the conversation
        content (str): The message content
        
    Returns:
        dict: The API response
    """
    url = "http://localhost:10088/api/chatbot/v1/chat"
    
    payload = {
        "conversation_id": conversation_id,
        "content": content,
        "suggested": 0,
        # "global_topic": global_topic
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers, stream=True)
        response.raise_for_status()
        
        # Process the streaming response
        full_response = ""
        for line in response.iter_lines():
            if line:
                # Remove 'data: ' prefix and decode
                text = line.decode()
                # print(text)
                logger.info(f"Token from chatbot API: {text}")
                if text:  # Skip end marker
                    full_response += text + "\n"
        main_response = full_response       
        
        notify_marker_index = main_response.find("<notify>")
        main_response = full_response[notify_marker_index + 9 if notify_marker_index != -1 else 0:]
        main_response = main_response[:main_response.find("<stop>")]
        
        return main_response 
    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")
        return None
    
async def reply_to_chat_message(chat_id: str, content: str, reply_to_id: Optional[str]) -> dict:
    """
    Reply to a chat message.
    
    Args:
        chat_id (str): The ID of the chat
        content (str): The message content
        
    Returns:
        dict: The API response
    """
    
    conversation = await mongo_service.get_by_chat_id(chat_id)

    repyly_content = send_chat_message_to_agent(conversation.conversation_id, content)
    # repyly_content = repyly_content.json()["content"]
    logger.info(f"Replying to chat message: {repyly_content}")
    
    payload = {}
    
    if reply_to_id is not None:
        payload = {
            "reply_to_message_id": reply_to_id
        }
    
    send_message(chat_id, repyly_content, payload)