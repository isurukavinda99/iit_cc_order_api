from sqlalchemy import Column, Integer, Float, ForeignKey, String
from sqlalchemy.orm import relationship
from app.config.config import Base

class OrderEntry(Base):
    __tablename__ = "order_entries"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id", ondelete="CASCADE"))
    game_id = Column(String(250), nullable=False)
    item_price = Column(Float, nullable=False)

    order = relationship("Order", back_populates="entries")
