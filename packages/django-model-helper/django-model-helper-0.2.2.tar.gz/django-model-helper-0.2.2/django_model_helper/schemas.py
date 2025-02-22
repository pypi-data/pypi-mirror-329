from typing import Optional
import datetime
import pydantic
from django.contrib.auth.models import User as DjangoUser


class UserBase(pydantic.BaseModel):
    username: Optional[str] = None

    def get_user_identify(self):
        """获取用户唯一码。"""
        return self.username

    @classmethod
    def from_dict(cls, data: dict):
        return cls.model_validate(data)

    @classmethod
    def from_str(cls, username: str):
        """根据str类型生成的用户对象。"""
        return cls.model_validate(
            {
                "username": username,
            }
        )

    @classmethod
    def from_django_user(cls, user: DjangoUser):
        """根据django对象生成的用户对象。"""
        return cls.model_validate(
            {
                "id": user.id,
                "username": user.username,
            }
        )


class User(UserBase):
    id: Optional[int] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    is_staff: Optional[bool] = None
    is_active: Optional[bool] = None
    is_superuser: Optional[bool] = None
    date_joined: Optional[datetime.datetime] = None
    last_login: Optional[datetime.datetime] = None

    @classmethod
    def from_int(cls, id: int):
        return cls.model_validate(
            {
                "id": id,
            }
        )

    @classmethod
    def from_django_user(cls, user: DjangoUser):
        """根据django对象生成的用户对象。"""
        return cls.model_validate(
            {
                "id": user.id,
                "username": user.username,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "is_staff": user.is_staff,
                "is_active": user.is_active,
                "is_superuser": user.is_superuser,
                "date_joined": user.date_joined,
                "last_login": user.last_login,
            }
        )
