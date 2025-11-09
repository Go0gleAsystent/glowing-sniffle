from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime


# ============ USERS ============
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        orm_mode = True


# ============ POSTS ============
class PostCreate(BaseModel):
    title: str
    content: str


class PostOut(BaseModel):
    id: int
    title: str
    content: str
    created_at: datetime
    user_id: int

    class Config:
        orm_mode = True


# ============ COMMENTS ============
class CommentCreate(BaseModel):
    content: str


class CommentOut(BaseModel):
    id: int
    content: str
    created_at: datetime
    user_id: int
    post_id: int

    class Config:
        orm_mode = True


# ============ JWT ============
class Token(BaseModel):
    access_token: str
    token_type: str
