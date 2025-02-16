from functools import lru_cache
from langfuse.decorators import observe
from models.documents import ConversationDocument
from models import Conversation
from typing import Optional
from uuid import uuid4

class MongoService:
    async def create_conversation(self, conversation: Conversation) -> ConversationDocument:
        # conversation = Conversation(conversation_id=conversation_id, customer_phone=customer_phone)

        # conversation.history.append(Message(role="Agent", content="Sapo xin nghe. Em có thể hỗ trợ gì được cho mình ạ."))

        new_conversation = ConversationDocument(conversation_id=conversation.conversation_id,
                                                    chat_id=conversation.chat_id,
                                                    created_at=conversation.created_at)
        await new_conversation.insert()
        
        return new_conversation
    
    async def get_by_chat_id(self, chat_id: str) -> Optional[Conversation]:
        conversation_document = await ConversationDocument.find(ConversationDocument.chat_id == chat_id).first_or_none()

        if conversation_document is not None:
            
            conversation = Conversation(conversation_id=conversation_document.conversation_id,
                                        chat_id=conversation_document.chat_id,
                                        created_at=conversation_document.created_at)
            
            return conversation
        
        
        conversation_id = str(uuid4())
        conversation = Conversation(conversation_id=conversation_id, chat_id=chat_id)
        
        new_conversation = await self.create_conversation(conversation)
        
        return new_conversation
        

    async def update_conversation(self, chat_id: str, conversation_id: str):
        conversation = await ConversationDocument.find(ConversationDocument.chat_id == chat_id).first_or_none()
        if conversation is not None:
            conversation.chat_id = chat_id
       
        await conversation.save()
        return True

mongo_service = MongoService()

@lru_cache(maxsize=None)
def get_mongo_service():
    return mongo_service


