from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr
from app.core.db import get_db  
from app.model.user import User
from app.schemas.user import UserUpdateDto, UserResponseDto
from app.schemas.user import UserRequestDto, UserResponseDto
from app.schemas.api_response import APIResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from app.core.auth_helper import hash_password
from app.core.secure import get_current_user
from app.core.db import get_db  
from app.model.user import User

user_router = APIRouter(
    prefix="/user",
)

@user_router.post("/", response_model=APIResponse)
async def create_user(user_request_dto: UserRequestDto, db: AsyncSession = Depends(get_db)):
    new_user = User(
        username=user_request_dto.username,
        email=user_request_dto.email,
        password=hash_password(user_request_dto.password)
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
    user.password = hash_password(user_request_dto.password)
    
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



@user_router.put("/me", response_model=APIResponse)
async def update_my_profile(
    user_request_dto: UserUpdateDto,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    current_user.username = user_request_dto.username
    current_user.email = user_request_dto.email

    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Email already exists"
        )

    await db.refresh(current_user)

    return APIResponse(
        status="success",
        message="Profile updated successfully",
        data={
            "user": UserResponseDto.model_validate(current_user)
        }
    )

    