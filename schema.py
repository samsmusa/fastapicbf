import datetime
from typing import Optional
from pydantic import BaseModel

import inspect
from typing import Type

from fastapi import Form
from pydantic.fields import ModelField


def as_form(cls: Type[BaseModel]):
    new_parameters = []

    for field_name, model_field in cls.__fields__.items():
        model_field: ModelField  # type: ignore

        new_parameters.append(
            inspect.Parameter(
                model_field.alias,
                inspect.Parameter.POSITIONAL_ONLY,
                default=Form(...) if model_field.required else Form(model_field.default),
                annotation=model_field.outer_type_,
            )
        )

    async def as_form_func(**data):
        return cls(**data)

    sig = inspect.signature(as_form_func)
    sig = sig.replace(parameters=new_parameters)
    as_form_func.__signature__ = sig  # type: ignore
    setattr(cls, 'as_form', as_form_func)
    return cls


class AuthGroup(BaseModel):
    id: int
    name: str
    active: int


class AuthenticationUser(BaseModel):
    id: int
    password: str
    last_login: Optional[datetime.datetime]
    is_superuser: int
    username: str
    first_name: str
    last_name: str
    is_staff: int
    is_active: int
    date_joined: datetime.datetime
    created_at: datetime.datetime
    updated_at: datetime.datetime
    email_verified_at: datetime.datetime
    email: str
    phone: Optional[str]
    profile_image: Optional[str]
    gender: Optional[str]
    birth_date: Optional[datetime.date]
    age: Optional[int]
    location: Optional[str]
    country_code: Optional[str]
    country: Optional[str]
    city: Optional[str]
    address: Optional[str]
    bio: Optional[str]


class AuthenticationUserGroups(BaseModel):
    id: int
    user_id: int
    group_id: int


class DjangoContentType(BaseModel):
    id: int
    app_label: str
    model: str


class AuthPermission(BaseModel):
    id: int
    name: str
    content_type_id: int
    codename: str


class AuthGroupPermissions(BaseModel):
    id: int
    group_id: int
    permission_id: int


class AuthenticationUserUserPermissions(BaseModel):
    id: int
    user_id: int
    permission_id: int


class DjangoAdminLog(BaseModel):
    id: int
    action_time: datetime.datetime
    object_id: Optional[str]
    object_repr: str
    action_flag: int
    change_message: str
    content_type_id: Optional[int]
    user_id: int


class DjangoMigrations(BaseModel):
    id: int
    app: str
    name: str
    applied: datetime.datetime


class DjangoSession(BaseModel):
    session_key: str
    session_data: str
    expire_date: datetime.datetime


@as_form
class FilterJob(BaseModel):
    id: Optional[int]
    title: Optional[str]
    description: str


class FilterJobprofile(BaseModel):
    id: int
    skills: str
    job_id: int


class FilterSkilltype(BaseModel):
    id: int
    type: Optional[str]


class FilterSkill(BaseModel):
    id: Optional[int]
    skill: Optional[str]
    type_id: int

    class Config:
        orm_mode = True


class FilterJobSkill(BaseModel):
    id: int
    job_id: int
    skill_id: int


class FilterYouth(BaseModel):
    id: int
    name: Optional[str]
    education_label: str
    education_field: str


class FilterYouthSkill(BaseModel):
    id: int
    youth_id: int
    skill: FilterSkill | None = None

    class Config:
        orm_mode = True


class FilterYouthprofile(BaseModel):
    id: int
    skills: str
    youth_id: int
