# Додайте цю модель до існуючого файлу models.py
from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class UsageLog(Base):
    """Лог використання AI для моніторингу витрат"""
    __tablename__ = "usage_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    request_type = Column(String, nullable=False)  # 'simple', 'detailed', 'average'
    tokens_used = Column(Integer, nullable=False)
    cost_usd = Column(Float, nullable=False)
    cost_eur = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    
    # Relationships
    user = relationship("User", back_populates="usage_logs")


# Додайте до моделі User:
class User(Base):
    # ... існуючі поля ...
    
    subscription_plan = Column(String, default='free')  # 'free', 'basic', 'standard', 'premium'
    subscription_expires = Column(DateTime, nullable=True)
    
    # Relationships
    usage_logs = relationship("UsageLog", back_populates="user")
