from fastapi import APIRouter, HTTPException, Body
from starlette import status
from schemas import SignUp
from controllers.auth import signUp


router = APIRouter()


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register_user(user_info: SignUp):
    """Register a new user"""
    return_val = signUp(
        user_info.name,
        user_info.email,
        user_info.password,
        user_info.wallet_status,
    )
    if return_val is None:
        raise HTTPException(400, detail="Cannot be registered!")
    else:
        return {
            "message": f"User with email {user_info.email} registered successfully!"
        }
