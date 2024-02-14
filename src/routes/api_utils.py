import functools
from typing import Annotated
from jose import jwt, JWTError
from fastapi import HTTPException, Depends
from starlette import status
from fastapi.security import OAuth2PasswordBearer


SECRET_KEY = "pratiksha"
ALGORITHM = "HS256"

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="/login")
token_dependency = Annotated[dict, Depends(oauth2_bearer)]


def get_jwt_identity(token: token_dependency):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("email")
        role: int = payload.get("role")
        if email is None or role is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate user.",
            )
        return email
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user."
        )


def role_required(roles_list):
    def inner(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                token = kwargs.get('token')
                payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
                role: str = payload.get("role")
                email: str = payload.get("email")
                if role is None or email is None:
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Could not validate user.",
                    )
                if role in roles_list:
                    return func(*args, **kwargs)
                else:
                    raise HTTPException(status_code=403, detail="Access denied")
            except JWTError:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Could not validate user.",
                )

        return wrapper
    return inner
