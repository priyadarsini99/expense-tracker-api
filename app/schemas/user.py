from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime


class UserRequestDto(BaseModel):
    username: str = Field(
        ...,
        min_length=3,
        max_length=50,
        description="Username of the user"
    )

    email: str = Field(
        ...,
        min_length=5,
        max_length=100,
        description="Email address of the user"
    )

    password: str = Field(
        ...,
        min_length=8,
        max_length=100,
        description="Password of the user"
    )


class UserResponseDto(BaseModel):
    id: int = Field(
        ...,
        description="ID of the user"
    )

    username: str = Field(
        ...,
        min_length=3,
        max_length=50,
        description="Username of the user"
    )

    email: str = Field(
        ...,
        min_length=5,
        max_length=100,
        description="Email address of the user"
    )

    created_at: datetime = Field(
        ...,
        description="Date and time when the user was created"
    )

    model_config = ConfigDict(from_attributes=True)


class LoginRequest(BaseModel):
        email: str = Field(
            ...,
            min_length=5,
            max_length=100,
            description="Email address of the user"
        )

        password: str = Field(
            ...,
            min_length=8,
            max_length=100,
            description="Password of the user"
        )


class LoginResponse(BaseModel):
    access_token: str = Field(
        ...,
        description="JWT access token for the user"
    )

    user: UserResponseDto 