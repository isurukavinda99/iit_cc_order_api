from sqlalchemy.orm import Session
from typing import List, Optional
from app.repositories.order_repository import OrderRepository
from app.entity.order_entries import OrderEntry
from app.entity.order_entity import Order
from app.dto.order_schema import OrderCreate

class OrderService:
    def __init__(self, repository: OrderRepository):
        self.repository = repository

    def create_order(self, db: Session, order_data: OrderCreate, invoke: str) -> Order:
        order_data.created_by = invoke
        return self.repository.create_order(db, order_data)

    def get_all_orders(self, db: Session) -> List[Order]:
        return self.repository.get_all_orders(db)

    def get_order_by_id(self, db: Session, order_id: int) -> Optional[Order]:
        return self.repository.get_order_by_id(db, order_id)
