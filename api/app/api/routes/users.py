from fastapi import APIRouter

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.post("/register")
def register_user(email: str, password: str):
    return {"email": email, "password": password}


@router.patch("/activate")
def activate_user(user_id: int, code: str):
    return {"code": code}
