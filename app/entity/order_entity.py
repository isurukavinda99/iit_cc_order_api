from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.config.config import Base

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    active = Column(Boolean, default=True)
    created_by = Column(String(250), nullable=True)
    updated_by = Column(String(250), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationship to order entries
    entries = relationship("OrderEntry", back_populates="order", cascade="all, delete-orphan")
