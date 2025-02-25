from beanie import Document
from datetime import datetime
from zoneinfo import ZoneInfo
from models import UserBotConversation
class ConversationDocument(Document):
    chat_id: int
    user_id: int
    conversation_id: str
    history: list[UserBotConversation] = []
    created_at: datetime = datetime.now(ZoneInfo("Asia/Ho_Chi_Minh"))

    class Settings:
        name = "conversation"
        indexes = [
            "chat_id",
            "user_id"
        ]