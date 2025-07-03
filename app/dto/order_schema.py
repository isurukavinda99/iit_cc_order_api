from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional, List

class OrderCreate(BaseModel):
    game_ids: List[str]
    item_prices: List[float]
    active: Optional[bool] = True
    created_by: Optional[str] = None
    updated_by: Optional[str] = None
