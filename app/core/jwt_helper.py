from datetime import datetime, timedelta ,timezone
from jose import jwt
from fastapi import HTTPException , status

SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES  = 30

#create access token
def create_access_token(data: dict, expires_delta: timedelta  | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str):
    try:
     payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
     return payload
    except jwt.JWTError:
        print("Invalid token")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

if __name__ == "__main__":
    print("Creating access token...")
    data = {"sub": "user_id"}
    token = create_access_token(data)
    verfy_token = verify_access_token(token)
    print("Token verified successfully:", verfy_token)
    