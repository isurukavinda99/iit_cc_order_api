from fastapi import APIRouter, Depends, HTTPException

router = APIRouter()
import logging
from app.config.config import get_db
from app.dto.order_schema import OrderCreate
from sqlalchemy.orm import Session
from app.middleware.alb_auth import require_auth
from app.services.order_service import OrderService
from app.repositories.order_repository import OrderRepository

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/order", tags=["order"])

order_service = OrderService(OrderRepository())

@router.post("/")
def create_order(order: OrderCreate, db: Session = Depends(get_db), claims: dict = Depends(require_auth)):
    return order_service.create_order(db=db, order_data=order, invoke=claims.get("email"))

@router.get("/")
def get_all_orders(db: Session = Depends(get_db), claims: dict = Depends(require_auth)):
    return order_service.get_all_orders(db=db, invoke=claims.get("email"))

@router.get("/{order_id}")
def get_order_by_id(order_id: int, db: Session = Depends(get_db), claims: dict = Depends(require_auth)):
    order = order_service.get_order_by_id(db=db, order_id=order_id, invoke=claims.get("email"))
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order