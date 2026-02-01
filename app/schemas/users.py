from pydantic import BaseModel, ConfigDict, EmailStr


class UserBase(BaseModel):
    firstname: str
    lastname: str | None = None
    patronymic: str | None = None
    email: EmailStr


class UserLogin(BaseModel):
    firstname: str
    email: EmailStr


class UserResponse(UserBase):
    role: str


class UserCreate(UserBase):
    password: str
    password_replay: str


class UserRead(UserBase):
    id: int
    is_active: bool
    role_id: int
    password_hash: str

    model_config = ConfigDict(from_attributes=True)


class UserUpdate(UserBase):
    firstname: str | None = None
    is_active: bool | None = None
    email: EmailStr | None = None
    # пароль и роль?
