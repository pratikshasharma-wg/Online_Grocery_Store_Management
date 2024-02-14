from fastapi import APIRouter, HTTPException, Body, Path, Depends
from starlette import status
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from routes.api_utils import get_jwt_identity
from controllers.order_controller import place_order, show_all_orders
from .api_utils import token_dependency, role_required


router = APIRouter()


@router.post("/orders", status_code=status.HTTP_201_CREATED)
def place_order_route(orders: Annotated[dict, Body()], email: Annotated[str, Depends(get_jwt_identity)]):
    if (place_order(orders["orders"], email)):
        return {
            "message": "Order Placed Successfully!"
        }
    else:
        return {
            "message" : "Please select atleast one product to place order"
        }
    

@router.get("/orders", status_code=status.HTTP_200_OK)
@role_required(["Admin"])
def fetch_orders(token: token_dependency):

    data = show_all_orders()
    if not data:
        return {
            "message": "Currently no orders place"
        }
    else:
        return {"orders": data}
