import requests
import json
from config.settings import settings
import logging
from services import mongo_service
# import mongo_service
from typing import Optional

TOKEN = settings.TELEGRAM_BOT_TOKEN
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TOKEN}/"

def send_message(chat_id, text, payload):
    """Send a message to a Telegram user."""
    url = TELEGRAM_API_URL + "sendMessage"
    payload = {"chat_id": chat_id, "text": text, **payload}
    requests.post(url, json=payload)

def send_chat_message_to_agent(conversation_id: str, content: str) -> dict:
    """
    Send a chat message to the chatbot API.
    
    Args:
        conversation_id (str): The ID of the conversation
        content (str): The message content
        
    Returns:
        dict: The API response
    """
    url = "http://54.158.157.54:10088/api/chatbot/v1/chat"
    
    payload = {
        "conversation_id": conversation_id,
        "content": content,
        "suggested": 0
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()  # Raise an exception for bad status codes
        return response
    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")
        return None
    
def reply_to_chat_message(chat_id: str, content: str, reply_to_id: Optional[str]) -> dict:
    """
    Reply to a chat message.
    
    Args:
        chat_id (str): The ID of the chat
        content (str): The message content
        
    Returns:
        dict: The API response
    """
    
    conversation = mongo_service.get_by_chat_id(chat_id)

    repyly_content = send_chat_message_to_agent(conversation.conversation_id, content)
    
    payload = {}
    
    if reply_to_id is not None:
        payload = {
            "reply_to_message_id": reply_to_id
        }
    
    send_message(chat_id, repyly_content, payload)