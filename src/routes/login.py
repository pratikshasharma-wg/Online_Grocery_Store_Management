from fastapi import APIRouter, HTTPException, Body
from starlette import status
from jose import jwt
from datetime import datetime, timedelta
from controllers.auth import login


router = APIRouter()


SECRET_KEY = "pratiksha"
ALGORITHM = "HS256"


@router.post("/login", status_code=status.HTTP_200_OK)
def login_user(user_info=Body()):

    return_val = login(user_info["email"], user_info["password"])

    if return_val is None or return_val is False:
        raise HTTPException(401, "Invalid Credentials!")
    else:
        token = create_access_token(return_val[1], return_val[2], timedelta(minutes=15))
        return {"access_token": token, "message": "User logged in successfully!"}


def create_access_token(role: str, email: str, expires_delta: timedelta):
    encode = {"role": role, "email": email}
    expires = datetime.utcnow() + expires_delta
    encode.update({"exp": expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)
