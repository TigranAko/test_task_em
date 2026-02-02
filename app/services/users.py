import bcrypt
import jwt
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from db.db import get_session
from sqlalchemy.orm import Session
from repositories.users import UserRepository
from schemas.users import UserCreate
from fastapi import Depends, HTTPException, status, Response
from services.roles import RoleService


class UserService:
    def __init__(self, session: Session):
        self.db: Session = session
        self.repo = UserRepository(session)
        self.secret_key = "your-secret-key"  # Вынеси в переменные окружения
        self.algorithm = "HS256"
        self.token_expire_hours = 24

    # 1. РЕГИСТРАЦИЯ
    def register(self, user: UserCreate):
        role_service = RoleService(self.db)
        role_id = role_service.repo.get_id("user")

        if user.password != user.password_replay:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Пароли не совпадают"
            )

        if self.repo.get_by_email(user.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Пользователь с таким email уже существует",
            )

        password_hash = self._hash_password(user.password)

        data = user.model_dump()
        data.pop("password")
        data.pop("password_replay")
        data["password_hash"] = password_hash
        data["role_id"] = role_id
        data["is_active"] = True

        result = self.repo.add_one(data)
        return result

    # 2. LOGIN (вход в систему)
    def login(self, email: str, password: str) -> str:
        """Возвращает JWT токен для установки в куки"""
        user = self.repo.get_by_email(email)

        if not user or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Неверный email или пароль",
            )

        if not self._verify_password(password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Неверный email или пароль",
            )

        # Создать JWT токен
        token = self._create_token(user.id)

        return token

    # 3. LOGOUT (выход из системы)
    def logout(self, response: Response):
        """Удаляет токен из куки"""
        # Просто удаляем куку - токен хранится на клиенте
        response.delete_cookie(key="access_token")
        return {"message": "Успешный выход из системы"}

    # 4. ОБНОВЛЕНИЕ ИНФОРМАЦИИ
    def update(self, user_id: int, update_data: Dict[str, Any]):
        user = self.repo.find_one(user_id)
        if not user or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден"
            )

        if "email" in update_data and update_data["email"] != user.email:
            if self.repo.get_by_email(update_data["email"]):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email уже используется",
                )

        updated_user = self.repo.edit_one(user_id, update_data)
        return updated_user

    # 5. УДАЛЕНИЕ ПОЛЬЗОВАТЕЛЯ (мягкое)
    def delete(self, user_id: int, current_password: Optional[str] = None):
        user = self.repo.find_one(user_id)

        if not user or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден"
            )

        # Проверка пароля перед удалением (опционально)
        if current_password:
            if not self._verify_password(current_password, user.password_hash):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверный пароль"
                )

        # Мягкое удаление
        self.repo.edit_one(user_id, {"is_active": False})

        return {"message": "Аккаунт успешно деактивирован"}

    # 6. ПОЛУЧЕНИЕ ТЕКУЩЕГО ПОЛЬЗОВАТЕЛЯ (из токена)
    def get_current_user(self, token: str):
        """Получает пользователя из JWT токена"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            user_id = payload.get("sub")

            if not user_id:
                return None

            user = self.repo.find_one(int(user_id))
            if not user or not user.is_active:
                return None

            return user

        except jwt.PyJWTError:
            return None

    # 7. УСТАНОВКА ТОКЕНА В КУКИ (для эндпоинтов)
    def set_auth_cookie(self, response: Response, token: str):
        """Устанавливает JWT токен в куки"""
        response.set_cookie(
            key="access_token",
            value=token,
            httponly=True,  # Защита от XSS
            max_age=self.token_expire_hours * 3600,
            expires=self.token_expire_hours * 3600,
            secure=False,  # True в production с HTTPS
            samesite="lax",
        )

    # Приватные методы
    def _hash_password(self, password: str) -> str:
        salt = bcrypt.gensalt()
        password_hash = bcrypt.hashpw(password.encode("utf-8"), salt)
        return password_hash.decode("utf-8")

    def _verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(
            plain_password.encode("utf-8"), hashed_password.encode("utf-8")
        )

    def _create_token(self, user_id: int) -> str:
        expires_delta = timedelta(hours=self.token_expire_hours)
        expire = datetime.utcnow() + expires_delta

        to_encode = {"sub": str(user_id), "exp": expire, "iat": datetime.utcnow()}

        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt


def get_user_service(session: Session = Depends(get_session)):
    return UserService(session)
