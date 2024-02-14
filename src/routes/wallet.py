from fastapi import APIRouter, HTTPException, Body, Path, Depends
from starlette import status
from typing import Annotated
from routes.api_utils import get_jwt_identity
from controllers.order_controller import get_wallet, update_wallet


router = APIRouter()


@router.get("/wallet", status_code=status.HTTP_200_OK)
def get_user_wallet(email: Annotated[str, Depends(get_jwt_identity)]):
    wallet_amount = get_wallet(email)
    
    return {"email": email, "wallet_amount": wallet_amount}
    

@router.put("/wallet", status_code=status.HTTP_200_OK)
def update_user_wallet(email: Annotated[str, Depends(get_jwt_identity)], amount=Body()):
    return_val = update_wallet(email, amount["amount"])
    if return_val:
        return {
            "email": email,
            "message": f"Amount of Rs.{amount['amount']} added to the wallet successfully!",
        }
    else:
        raise HTTPException(400, detail="Try again!")
