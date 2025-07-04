from sqlalchemy.orm import Session
from typing import List, Optional

from app.entity.order_entries import OrderEntry
from app.entity.order_entity import Order
from app.dto.order_schema import OrderCreate
from sqlalchemy.orm import joinedload
from sqlalchemy.orm import joinedload


class OrderRepository:

    def create_order(self, db: Session, order_data: OrderCreate) -> Order:
        new_order = Order(
            active=order_data.active,
            created_by=order_data.created_by,
            updated_by=order_data.updated_by,
        )
        db.add(new_order)
        db.flush()  # Ensure new_order.id is generated before adding entries

        # Add order entries
        for game_id, price in zip(order_data.game_ids, order_data.item_prices):
            entry = OrderEntry(
                order_id=new_order.id,
                game_id=game_id,
                item_price=price
            )
            db.add(entry)

        db.commit()
        db.refresh(new_order)
        return new_order

    def get_all_orders(self, db: Session, invoke: str) -> List[Order]:
        return (db.query(Order)
                .options(joinedload(Order.entries))
                .filter(Order.created_by == invoke)
                .all())

    def get_order_by_id(self, db: Session, order_id: int, invoke: str) -> Optional[Order]:
        return (
            db.query(Order)
                .options(joinedload(Order.entries))
                .filter(
                    (Order.id == order_id)&
                    (Order.created_by == invoke)
                )
                .first()
        )
