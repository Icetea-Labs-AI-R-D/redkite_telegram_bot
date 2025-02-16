from beanie import Document
from datetime import datetime
from zoneinfo import ZoneInfo

class ConversationDocument(Document):
    chat_id: int
    conversation_id: str
    created_at: datetime = datetime.now(ZoneInfo("Asia/Ho_Chi_Minh"))

    class Settings:
        name = "conversation"
        indexes = [
            "chat_id",
        ]