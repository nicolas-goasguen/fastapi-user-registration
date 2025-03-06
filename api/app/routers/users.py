from fastapi import APIRouter, HTTPException

from app.schemas.users import UserRegister, UserActivate
from app.services import users as users_services

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.get("/")
async def read_all_users():
    return await users_services.get_all_users()


@router.post("/register")
async def register_user(user_in: UserRegister):
    user = await users_services.get_user_by_email(user_in.email)
    if user:
        raise HTTPException(status_code=400, detail="Email already in use.")
    return await users_services.register_user(user_in)


@router.patch("/activate")
async def activate_user(user_in: UserActivate):
    return await users_services.register_user(user_in)
