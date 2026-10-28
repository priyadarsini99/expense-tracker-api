from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.jwt_helper import create_access_token
from app.schemas.user import LoginRequest, LoginResponse, UserResponseDto
from app.model.user import User
from app.core.db import get_db
from app.core.auth_helper import verify_password

auth_router = APIRouter(
    prefix = "/auth",
    tags = ["Authentication"]
)

@auth_router.post("/login" ,response_model=LoginResponse)
async def login_user(login_request : LoginRequest , db : AsyncSession = Depends(get_db)):
    # Logic for user login
    user = await db.execute(
        select(User).filter(User.email == login_request.email)
    )
    user = user.scalar_one_or_none()
    if not user or not verify_password(login_request.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    # Here you would typically verify the password
    # For example: if not verify_password(login_request.password, user.hashed_password):
    #     raise HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED,
    #         detail="Invalid email or password"
    #     

    access_token = create_access_token(data={
        "user_id": user.id,
        "sub": user.email
    })

    return LoginResponse(access_token=access_token, user=UserResponseDto.model_validate(user)
                         )