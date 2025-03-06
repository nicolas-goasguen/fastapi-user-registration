from fastapi import APIRouter, HTTPException

from app.core.db import database
from app.schemas.users import User, UserRegister, UserActivate
from app.services import users as users_services

router = APIRouter(
    prefix="/users",
    tags=["users"],
)

@router.get("/read")
async def read_all_users():
    return await users_services.get_all_users()

@router.post("/register")
async def register_user(user_in: UserRegister):
    return await users_services.register_user(user_in)


@router.patch("/activate")
async def activate_user(user_in: UserActivate):
    return await users_services.register_user(user_in)
