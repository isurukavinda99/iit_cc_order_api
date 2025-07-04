from typing import List, Optional

from sqlalchemy.orm import Session

from app.dto.order_schema import OrderCreate
from app.entity.order_entity import Order
from app.repositories.order_repository import OrderRepository


class OrderService:
    def __init__(self, repository: OrderRepository):
        self.repository = repository

    def create_order(self, db: Session, order_data: OrderCreate, invoke: str) -> Order:
        order_data.created_by = invoke
        return self.repository.create_order(db, order_data)

    def get_all_orders(self, db: Session, invoke: str, status: str) -> List[Order]:
        return self.repository.get_all_orders(db=db, invoke= invoke, status=status)

    def get_order_by_id(self, db: Session, order_id: int, invoke: str) -> Optional[Order]:
        return self.repository.get_order_by_id(db=db, order_id=order_id, invoke=invoke)
