from fastapi import APIRouter, Depends, HTTPException
from app.core.secure import get_current_user
from app.core.db import get_db  
from app.model.user import User
from app.schemas.expense import ExpenseRequestDto, ExpenseResponseDto
from app.model.expense import Expense
from app.schemas.api_response import APIResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

expense_router = APIRouter(
    prefix="/expense",
)


@expense_router.post("/" , response_model=APIResponse)
async def create_expense(expense_request_dto: ExpenseRequestDto, db: AsyncSession = Depends(get_db) ,  user: User = Depends(get_current_user)):
    
    new_expense = Expense(
        title=expense_request_dto.title,
        description=expense_request_dto.description,
        amount=expense_request_dto.amount,
        user_id=user.id
    )
    db.add(new_expense)
    await db.commit()
    await db.refresh(new_expense)
    print("new_expense has been created ")
    return APIResponse(
        status="success",message="Expense created successfully", data={
        "expense": ExpenseResponseDto.model_validate(new_expense)
    }
    )

#get all exenses

@expense_router.get("/", response_model=APIResponse)
async def get_all_expenses(db: AsyncSession = Depends(get_db)):
      result = await db.execute(select(Expense))
      expenses = result.scalars().all()
      return APIResponse(
        
        status="success",
        message="Expenses retrieved successfully",
        data={"expenses": [ExpenseResponseDto.model_validate(expense) for expense in expenses]}
    )

#get exense by id
@expense_router.get("/{expense_id}", response_model=APIResponse)
async def get_expense_by_id(expense_id: int, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    result = await db.execute(result = await db.execute(
    select(Expense).where(
        Expense.id == expense_id,
        Expense.user_id == user.id
    )
))
    expense = result.scalar_one_or_none()
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    return APIResponse(
        status="success",
        message="Expense retrieved successfully",
        data={"expense": ExpenseResponseDto.model_validate(expense)}
    )

#update expense by id
@expense_router.put("/{expense_id}", response_model=APIResponse)
async def update_expense_by_id(expense_id: int, expense_request_dto: ExpenseRequestDto, db: AsyncSession = Depends(get_db)):
    result = await db.execute(result = await db.execute(
    select(Expense).where(
        Expense.id == expense_id,
        Expense.user_id == user.id
    )
))
    expense = result.scalar_one_or_none()
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    
    expense.title = expense_request_dto.title
    expense.description = expense_request_dto.description
    expense.amount = expense_request_dto.amount
   
    
    
    await db.commit()
    await db.refresh(expense)
    
    return APIResponse(
        status="success",
        message="Expense updated successfully",
        data={"expense": ExpenseResponseDto.model_validate(expense)}
    )

#delete expense by id
@expense_router.delete("/{expense_id}", response_model=APIResponse )     
async def delete_expense_by_id(expense_id: int, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    result = await db.execute(result = await db.execute(
    select(Expense).where(
        Expense.id == expense_id,
        Expense.user_id == user.id
    )
))
    expense = result.scalar_one_or_none()
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    
    await db.delete(expense)
    await db.commit()
    
    return APIResponse(
        status="success",
        message="Expense deleted successfully",
        data={"expense": ExpenseResponseDto.model_validate(expense)}
    )

