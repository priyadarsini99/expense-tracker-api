from fastapi import APIRouter, Depends, HTTPException, status 
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials 
from sqlalchemy import select
from app.core.db import get_db
from sqlalchemy.ext.asyncio import AsyncSession

security_scheme = HTTPBearer()

async def get_current_user(  credentials: HTTPAuthorizationCredentials = Depends(security_scheme),
    db: AsyncSession = Depends(get_db)
):
        from app.core.jwt_helper import verify_access_token
        from app.model.user import User
        token = credentials.credentials
        try:
            payload = verify_access_token(token = token)
            user_id = payload.get("user_id")
            if user_id is None:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

            result = await db.execute(
                select(User).where(User.id == user_id))
            user = result.scalar_one_or_none()
            if user is None:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

            return user
        except HTTPException:
            raise
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
            ) from exc

        