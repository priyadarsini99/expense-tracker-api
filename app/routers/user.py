from fastapi import APIRouter, Depends, HTTPException

from app.core.db import get_db  
from app.model.user import User
from app.schemas.user import UserRequestDto, UserResponseDto
from app.schemas.api_response import APIResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

user_router = APIRouter(
    prefix="/user",
)

@user_router.post("/", response_model=APIResponse)
async def create_user(user_request_dto: UserRequestDto, db: AsyncSession = Depends(get_db)):
    new_user = User(
        username=user_request_dto.username,
        email=user_request_dto.email,
        password=user_request_dto.password
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return APIResponse(
        status="success",
        message="User created successfully",
        data={"user": UserResponseDto.model_validate(new_user)}
    )


@user_router.get("/", response_model=APIResponse)
async def get_all_users(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User))
    users = result.scalars().all()
    return APIResponse(
        status="success",
        message="Users retrieved successfully",
        data={"users": [UserResponseDto.model_validate(user) for user in users]}
    )


@user_router.get("/{user_id}", response_model=APIResponse)
async def get_user_by_id(user_id: int, db: AsyncSession = Depends(get_db )):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return APIResponse(
        status="success",
        message="User retrieved successfully",
        data={"user": UserResponseDto.model_validate(user)}
    )

@user_router.put("/{user_id}", response_model=APIResponse)
async def update_user_by_id(user_id: int, user_request_dto: UserRequestDto, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.username = user_request_dto.username
    user.email = user_request_dto.email
    user.password = user_request_dto.password
    
    await db.commit()
    await db.refresh(user)
    
    return APIResponse(
        status="success",
        message="User updated successfully",
        data={"user": UserResponseDto.model_validate(user)}
    )

@user_router.delete("/{user_id}", response_model=APIResponse)
async def delete_user_by_id(user_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    await db.delete(user)
    await db.commit()
    
    return APIResponse(
        status="success",
        message="User deleted successfully"
    )

