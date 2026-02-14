from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from uuid import uuid4

app = FastAPI(title="AI Test Demo API")

fake_orders_db = {}

class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)

class OrderCreate(BaseModel):
    item_id: str = Field(min_length=1)
    quantity: int = Field(ge=1, le=10)

class OrderOut(BaseModel):
    order_id: str
    item_id: str
    quantity: int


@app.post("/auth/login")
def login(req: LoginRequest):
    if req.email == "user@test.com" and req.password == "secret123":
        return {"access_token": "testtoken"}

    raise HTTPException(status_code=401, detail="Invalid credentials")


@app.post("/orders", status_code=201, response_model=OrderOut)
def create_order(
    order: OrderCreate,
    authorization: Optional[str] = Header(None)
):
    if authorization != "Bearer testtoken":
        raise HTTPException(status_code=401, detail="Unauthorized")

    # business rule (not schema)
    if order.item_id.upper() == "BLOCKED":
        raise HTTPException(status_code=400, detail="Item is blocked")

    order_id = str(uuid4())

    fake_orders_db[order_id] = {
        "order_id": order_id,
        "item_id": order.item_id,
        "quantity": order.quantity,
    }

    return fake_orders_db[order_id]


@app.get("/orders/{order_id}", response_model=OrderOut)
def get_order(order_id: str, authorization: Optional[str] = Header(None)):
    if authorization != "Bearer testtoken":
        raise HTTPException(status_code=401, detail="Unauthorized")

    if order_id not in fake_orders_db:
        raise HTTPException(status_code=404, detail="Order not found")

    return fake_orders_db[order_id]

