from fastapi import APIRouter, Depends, HTTPException, Response, Request, status
from schemas.users import UserCreate, UserLogin, UserUpdate, UserRead
from services.users import UserService, get_user_service

router = APIRouter(tags=["User"], prefix="/user")


# Dependency для получения текущего пользователя
async def get_current_user(
    request: Request, service: UserService = Depends(get_user_service)
):
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Не авторизован"
        )

    user = service.get_current_user(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный или просроченный токен",
        )
    return user


@router.post("/register")
async def register(user: UserCreate, service: UserService = Depends(get_user_service)):
    return service.register(user)


@router.post("/login")
async def login(
    credentials: UserLogin,
    response: Response,
    service: UserService = Depends(get_user_service),
):
    token = service.login(credentials.email, credentials.password)
    service.set_auth_cookie(response, token)
    return {"message": "Успешный вход"}


@router.post("/logout")
async def logout(response: Response, service: UserService = Depends(get_user_service)):
    return service.logout(response)


@router.put("/profile")
async def update_profile(
    update_data: UserUpdate,
    current_user: UserRead = Depends(get_current_user),
    service: UserService = Depends(get_user_service),
):
    return service.update(current_user.id, update_data.model_dump(exclude_none=True))


@router.delete("/profile")
async def delete_profile(
    request: Request,
    current_password: str | None = None,
    current_user=Depends(get_current_user),
    service: UserService = Depends(get_user_service),
):
    response = service.delete(current_user.id, current_password)

    # После удаления аккаунта выходим из системы
    token = request.cookies.get("access_token")
    if token:
        response_obj = Response(content=response["message"])
        service.logout(response_obj)
        return response_obj

    return response
