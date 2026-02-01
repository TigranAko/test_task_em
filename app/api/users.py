from fastapi import APIRouter, Depends
from schemas.users import UserCreate, UserLogin, UserUpdate
from services.users import UserService, get_user_service

router = APIRouter(tags=["User"], prefix="/user")


@router.post("/register")
def create_user(
    user: UserCreate, user_service: UserService = Depends(get_user_service)
):
    return user_service.register(user)


@router.get("/me")
def about_user(user_service: UserService = Depends(get_user_service)):
    return user_service.about()


@router.post("/login")
def login_user(user: UserLogin, user_service: UserService = Depends(get_user_service)):
    return user_service.login(user)


@router.delete("/logout")
def logout_user(user_service: UserService = Depends(get_user_service)):
    return user_service.logout()


@router.put("/update")
def update_user(
    user: UserUpdate, user_service: UserService = Depends(get_user_service)
):
    return user_service.update(user)


@router.patch("/update")
def part_update_user(
    user: UserUpdate, user_service: UserService = Depends(get_user_service)
):
    return user_service.update(user)
