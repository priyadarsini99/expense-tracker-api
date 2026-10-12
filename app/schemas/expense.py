from pydantic import BaseModel ,Field,ConfigDict
from datetime import date as DateType

class ExpenseRequestDto(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    amount: float = Field(..., gt=0)
    description: str | None = Field(None, max_length=500)

class ExpenseResponseDto(BaseModel):
    id: int=Field(..., description="ID of the expense") 
    title: str=Field(..., description="Title of the expense" , min_length=1, max_length=100)
    amount: float=Field(..., description="Amount of the expense", gt=0)
    description: str = Field(None, description="Description of the expense", max_length=500)
    date: DateType =Field(..., description="Date of the expense in YYYY-MM-DD format")
    model_config = ConfigDict(from_attributes=True)