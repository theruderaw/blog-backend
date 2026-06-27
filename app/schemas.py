from pydantic import BaseModel
from typing import Any
from uuid import UUID

class RequestModel(BaseModel):
    user_uuid : UUID

class UserReference(BaseModel):
    uuid : UUID

class CreateArticle(RequestModel):
    title : str
    slug : str
    status : str|None = 'draft'
    body : list[Any]
    
class EditArticle(RequestModel):
    title : str | None = None
    slug : str | None = None
    status : str | None = None
    body : list[Any] | None = None

class DeleteArticle(RequestModel):
    article_id : UUID

class MessageModel(UserReference):
    sender_name : str
    sender_email : str
    message_text : str