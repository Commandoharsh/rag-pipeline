from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from backend.api.auth import decode_access_token
from backend.api.dependencies import get_current_user
from backend.database.auth_service import AuthService
from backend.database.database import Database
from backend.database.user_repository import UserRepository


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


database = Database()

repository = UserRepository(
    database
)

auth_service = AuthService(
    repository
)


class RegisterRequest(BaseModel):
    email: str
    password: str = Field(min_length=8)


class LoginRequest(BaseModel):
    email: str
    password: str


@router.post("/register")
def register(request: RegisterRequest):

    try:
        user = auth_service.register(
            request.email,
            request.password,
        )

        return {
            "id": user.id,
            "email": user.email,
            "is_active": user.is_active,
        }

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )

    except Exception as exc:
        print(
            f"[AUTH REGISTER ERROR] "
            f"{type(exc).__name__}: {exc}"
        )

        raise HTTPException(
            status_code=500,
            detail=(
                "Registration failed due to "
                f"{type(exc).__name__}: {exc}"
            ),
        )


@router.post("/login")
def login(request: LoginRequest):

    result = auth_service.authenticate(
        request.email,
        request.password,
    )

    if result is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password.",
        )

    return result


@router.get("/me")
def get_me(
    current_user=Depends(get_current_user),
):
    return {
        "id": current_user.id,
        "email": current_user.email,
        "is_active": current_user.is_active,
        "created_at": current_user.created_at,
    }


@router.get("/verify")
def verify_token(token: str):

    payload = decode_access_token(
        token
    )

    if payload is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token.",
        )

    return {
        "valid": True,
        "user_id": payload["sub"],
    }