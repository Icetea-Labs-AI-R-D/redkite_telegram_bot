from datetime import datetime
from pydantic import BaseModel
from zoneinfo import ZoneInfo
from typing import Optional
class UserBotConversation(BaseModel):
    bot_message_id: int
    user_message: str
    bot_message: str
    global_topic: Optional[dict] = None


class Conversation(BaseModel):
    chat_id: int
    user_id: int
    conversation_id: str
    history: list[UserBotConversation] = []
    created_at: datetime = datetime.now(ZoneInfo("Asia/Ho_Chi_Minh"))