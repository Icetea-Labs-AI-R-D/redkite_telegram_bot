from datetime import datetime
from pydantic import BaseModel
from zoneinfo import ZoneInfo

class Conversation(BaseModel):
    conversation_id: str
    chat_id: str
    created_at: datetime = datetime.now(ZoneInfo("Asia/Ho_Chi_Minh"))