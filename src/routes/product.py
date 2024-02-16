from fastapi import APIRouter, HTTPException, Body, Path, Depends
from starlette import status
from schemas import AddProduct
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from controllers.product_controller import (
    add_product,
    delete_product,
    update_product,
    show_all_products,
)

from .api_utils import token_dependency, role_required


router = APIRouter()


@router.post("/products", status_code=status.HTTP_200_OK)
@role_required(["Admin"])
def add_products(product_info: AddProduct, token:token_dependency):
    return_val = add_product(
        product_info.product_name,
        product_info.product_price,
        product_info.product_quantity,
    )

    if return_val is True:
        return {
            "message": "New product added successfully!"
        }
    else:
        raise HTTPException(404, detail="Product not added")


@router.delete("/products/{product_id}", status_code=status.HTTP_200_OK)
@role_required(["Admin"])
def delete_products(token: token_dependency, product_id=Path()):
    return_val = delete_product(product_id)

    if return_val is True:
        return {
            "message": f"Product with Product id:{product_id} deleted successfully!!!"
        }
    else:
        raise HTTPException(400, detail="Product does not exists!")


@router.put("/products/{product_id}", status_code=status.HTTP_200_OK)
@role_required(["Admin"])
def update_products(token: token_dependency, product_info=Body(), product_id=Path()):
    product_name = product_info.get('product_name')
    product_price = product_info.get('product_price')
    product_quantity = product_info.get('product_quantity')

    return_val = update_product(
        product_id, product_name, product_price, product_quantity
    )
    if return_val is True:
        return {"message": "Product details updated successfully!"}
    else:
        raise HTTPException(400, detail="Try again!")


@router.get("/products", status_code=status.HTTP_200_OK)
@role_required(["Admin", "Customer"])
def get_products(token: token_dependency):
    return_val = show_all_products()
    if return_val is not None:
        return {"products": return_val}
    else:
        raise HTTPException(400, detail="Try again!")
