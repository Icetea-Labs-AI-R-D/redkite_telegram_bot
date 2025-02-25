import requests
import json
from config.settings import settings
import logging
from services import mongo_service
# import mongo_service
from typing import Optional
import logging
from models import UserBotConversation

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

def send_chat_message_to_agent(conversation_id: str, content: str, replied_conversation: list[dict] = [], replied_conversation_global_topic:dict = {}) -> dict:
    """
    Send a chat message to the chatbot API.
    
    Args:
        conversation_id (str): The ID of the conversation
        content (str): The message content
        
    Returns:
        dict: The API response
    """
    url = "http://localhost:10088/api/chatbot/v1/tele-chat"
    
    payload = {
        "conversation_id": conversation_id,
        "content": content,
        "suggested": 0,
        "replied_conversation": replied_conversation,
        "replied_conversation_global_topic": replied_conversation_global_topic
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers, stream=True)
        response.raise_for_status()
        
        # Process the streaming response
        # full_response = ""
        # for line in response.iter_lines():
        #     if line:
        #         # Remove 'data: ' prefix and decode
        #         text = line.decode()
        #         # print(text)
        #         logger.info(f"Token from chatbot API: {text}")
        #         if text:  # Skip end marker
        #             full_response += text + "\n"
        # main_response = full_response      
        
        response_json = response.json()
        
        answer = response_json["data"]["answer"] 
        global_topic = response_json["data"]["global_topic"]
        main_response = answer
        
        notify_marker_index = main_response.find("</notify>")
        main_response = main_response[notify_marker_index + 9 if notify_marker_index != -1 else 0:]
        main_response = main_response[:main_response.find("<stop>")]
        
        return main_response, global_topic
    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")
        return None
    
async def reply_to_chat_message(chat_id: int, user_id: int, content: str, reply_to_id: Optional[int]=None, bot_replied_message_id: Optional[int]=None) -> dict:
    """
    Reply to a chat message.
    
    Args:
        chat_id (str): The ID of the chat
        content (str): The message content
        
    Returns:
        dict: The API response
    """
    
    conversation = await mongo_service.get_by_chat_id_user_id(chat_id, user_id)
    logger.info(f"Conversation: {conversation}")
    replied_conversation = []
    replied_conversation_global_topic = None
    logger.info(f"Bot replied message ID: {bot_replied_message_id}")
    
    for conv in conversation.history[::-1]:
        if conv.bot_message_id == bot_replied_message_id:
            replied_conversation = [
                {"role": "user", "content": conv.user_message},
                {"role": "assistant", "content": conv.bot_message}
            ]
            replied_conversation_global_topic = conv.global_topic
            logger.info(f"Replied conversation: {json.dumps(replied_conversation, ensure_ascii=False, indent=2)}")
            break

    repyly_content, global_topic = send_chat_message_to_agent(conversation.conversation_id, content, replied_conversation, replied_conversation_global_topic)
    # repyly_content = repyly_content.json()["content"]
    logger.info(f"Replying to chat message: {repyly_content}")
    
    payload = {}
    
    if reply_to_id is not None:
        payload = {
            "reply_to_message_id": reply_to_id
        }
    
    res = send_message(chat_id, repyly_content, payload)
    
    res_json = res.json()
    
    bot_message_id = res_json["result"]["message_id"]
    user_message = content
    bot_message = res_json["result"]["text"]
    
    user_bot_conversation = UserBotConversation(
        user_message=user_message,
        bot_message=bot_message,
        bot_message_id=bot_message_id,
        global_topic=global_topic
    )
    
    conversation.history.append(user_bot_conversation)
    
    await mongo_service.update_conversation(chat_id, user_id, conversation)

    