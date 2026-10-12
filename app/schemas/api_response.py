from typing import Optional
from pydantic import BaseModel

class APIResponse(BaseModel):
    status: str
    message: str
    data: Optional[dict] = None