from fastapi import FastAPI
from routes.login import router as login
from routes.register import router as register
from routes.product import router as product
from routes.order import router as order
from routes.wallet import router as wallet


app = FastAPI()


app.include_router(login)
app.include_router(register)
app.include_router(product)
app.include_router(order)
app.include_router(wallet)
