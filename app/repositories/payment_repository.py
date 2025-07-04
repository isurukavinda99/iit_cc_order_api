from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.entity.payment_entity import Payment
from app.exceptions.exceptions import AppExceptionCase


class PaymentRepository:

    def make_payment(self, db: Session, payment: Payment) -> Payment:
        try:
            db.add(payment)
            db.commit()
            db.refresh(payment)
            return payment

        except IntegrityError as e:
            db.rollback()
            if "foreign key constraint" in str(e).lower():
                raise AppExceptionCase(
                    message="Invalid order_id: referenced order does not exist.",
                    code="ORDER_NOT_FOUND"
                )
            else:
                raise AppExceptionCase(
                    message="Database integrity error.",
                    code="INTEGRITY_ERROR"
                )

        except Exception as e:
            db.rollback()
            raise AppExceptionCase(
                message="Unexpected error while processing payment.",
                code="UNEXPECTED_ERROR"
            )