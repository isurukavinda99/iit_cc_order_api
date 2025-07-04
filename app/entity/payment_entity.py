from sqlalchemy import Column, Integer, Boolean, String, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.config.config import Base

class Payment(Base):
    __tablename__ = "payment"

    id = Column(Integer, primary_key=True, index=True)
    payment_id= Column(String(250), nullable=False)
    payment_date = Column(DateTime(timezone=True), nullable=False)
    verify_signature = Column(String(250), nullable=False)
    payment_amount = Column(Float, nullable=False)
    order_id = Column(Integer, ForeignKey("orders.id", ondelete="CASCADE"), nullable=False)
    payment_status = Column(Boolean, nullable=False)

    created_by = Column(String(250), nullable=True)
    updated_by = Column(String(250), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    order = relationship("Order", back_populates="payments")
