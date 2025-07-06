from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.dto.payment_schema import MakePayment
from app.config.config import get_db
from app.middleware.alb_auth import require_auth
from app.repositories.payment_repository import PaymentRepository
from app.repositories.order_repository import OrderRepository
from app.services.payment_service import PaymentService

router = APIRouter(prefix="/payment", tags=["payment"])

payment_service = PaymentService(paymentRepo=PaymentRepository(), orderRepo=OrderRepository())

@router.post("/")
def make_payment(make_payment: MakePayment, db: Session = Depends(get_db), claims: dict = Depends(require_auth)):
    return payment_service.make_payment(db=db, payment_dto=make_payment, invoker=claims.get("email"))