from datetime import datetime
from pydantic import BaseModel
from zoneinfo import ZoneInfo



class Conversation(BaseModel):
    chat_id: int
    conversation_id: str
    # history: list = []
    created_at: datetime = datetime.now(ZoneInfo("Asia/Ho_Chi_Minh"))