from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.config.config import Base
from app.entity.EntryStatus import EntryStatus


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    active = Column(Boolean, default=True)
    created_by = Column(String(250), nullable=True)
    updated_by = Column(String(250), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    status = Column(SQLEnum(EntryStatus), nullable=False, default=EntryStatus.PENDING)

    # Relationship to order entries
    entries = relationship("OrderEntry", back_populates="order", cascade="all, delete-orphan")
    payments = relationship("Payment", back_populates="order", cascade="all, delete-orphan")
