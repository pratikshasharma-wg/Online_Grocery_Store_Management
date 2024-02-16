from pydantic import BaseModel


class SignUp(BaseModel):
    name: str
    email: str
    password: str
    wallet_status: int


class SignIn(BaseModel):
    email: str
    password: str


class UpdateWallet(BaseModel):
    amount: int


class AddProduct(BaseModel):
    product_name: str
    product_price: int
    product_quantity: int
