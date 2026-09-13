from database.database import Base
from sqlalchemy import Column,String,Integer,Boolean,DateTime,ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

class User(Base):
    __tablename__="users"

    id=Column(Integer,primary_key=True,autoincrement=True)
    name=Column(String(200),nullable=False)
    email=Column(String(200),nullable=False,unique=True)
    password=Column(String(255),nullable=True)
    google_id=Column(String(255),unique=True,index=True,nullable=True)
    picture=Column(String(1000))
    is_active=Column(Boolean,default=True)
    created_at=Column(DateTime,default=datetime.utcnow)
    updated_at=Column(DateTime,default=datetime.utcnow,onupdate=datetime.utcnow)

    refresh_tokens=relationship("RefreshToken",back_populates="user",cascade="all,delete-orphan")

class RefreshToken(Base):
    __tablename__="refresh_tokens"

    id=Column(Integer,primary_key=True,autoincrement=True)
    user_id=Column(Integer,ForeignKey("users.id"),nullable=False,index=True)
    token_hash=Column(String(64),unique=True,nullable=False,index=True)
    expires_at=Column(DateTime,nullable=False)
    created_at=Column(DateTime,default=datetime.utcnow,nullable=False)
    revoked_at=Column(DateTime,nullable=True)
    replaced_by=Column(Integer,ForeignKey("refresh_tokens.id"),nullable=True)

    user=relationship("User",back_populates="refresh_tokens")