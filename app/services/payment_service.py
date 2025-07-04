from sqlalchemy.orm import Session

from app.dto.payment_schema import MakePayment
from app.entity.payment_entity import Payment
from app.repositories.payment_repository import PaymentRepository


class PaymentService:
    def __init__(self, repository: PaymentRepository):
        self.repository = repository

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

        return self.repository.make_payment(db=db, payment=payment_ent)