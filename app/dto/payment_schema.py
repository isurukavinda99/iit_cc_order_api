from datetime import datetime

from pydantic import BaseModel


class MakePayment(BaseModel):
    payment_id: str
    payment_date: datetime
    verify_signature: str
    payment_amount: float
    order_id: int
    payment_status: bool