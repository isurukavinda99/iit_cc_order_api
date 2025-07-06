from sqlalchemy.orm import Session

from app.dto.payment_schema import MakePayment
from app.entity.EntryStatus import EntryStatus
from app.entity.payment_entity import Payment
from app.repositories.payment_repository import PaymentRepository
from app.repositories.order_repository import OrderRepository


class PaymentService:
    def __init__(self, paymentRepo: PaymentRepository, orderRepo: OrderRepository):
        self.paymentRepo = paymentRepo
        self.orderRepo = orderRepo

    def make_payment(self, db: Session, payment_dto: MakePayment, invoker: str):
        payment_ent = Payment(
            payment_id=payment_dto.payment_id,
            payment_date=payment_dto.payment_date,
            verify_signature=payment_dto.verify_signature,
            order_id=payment_dto.order_id,
            payment_status=payment_dto.payment_status,
            created_by=invoker,
            payment_amount=payment_dto.payment_amount
        )

        self.orderRepo.update_order_status(db=db, order_id=payment_dto.order_id, new_status=EntryStatus.COMPLETED)

        return self.paymentRepo.make_payment(db=db, payment=payment_ent)