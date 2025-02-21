from typing import Any

import httpx
import structlog
from fastapi import APIRouter, Depends, HTTPException, Response
from sqlmodel import col, delete, func, select

from mtmai.core.config import settings
from mtmai.core.security import get_password_hash, verify_password
from mtmai.crud import curd
from mtmai.crud.curd_account import get_account_by_user_id
from mtmai.deps import (
    AsyncSessionDep,
    CurrentUser,
    OptionalUserDep,
    SessionDep,
    get_current_active_superuser,
)
from mtmai.models.models import (
    Item,
    Message,
    UpdatePassword,
    User,
    UserCreate,
    UserPublic,
    UserRegister,
    UsersPublic,
    UserUpdate,
    UserUpdateMe,
)

# from mtmai.utils import generate_new_account_email, send_email
# from mtmlib.github import get_github_user_data

router = APIRouter()

# logger = logging.getLogger()
LOG = structlog.get_logger()


@router.get(
    "/",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=UsersPublic,
)
def read_users(session: SessionDep, skip: int = 0, limit: int = 100) -> Any:
    """
    Retrieve users.
    """
    count_statement = select(func.count()).select_from(User)
    count = session.exec(count_statement).one()

    statement = select(User).offset(skip).limit(limit)
    users = session.exec(statement).all()

    return UsersPublic(data=users, count=count)


@router.post(
    "/", dependencies=[Depends(get_current_active_superuser)], response_model=UserPublic
)
async def create_user(*, session: AsyncSessionDep, user_in: UserCreate) -> Any:
    """
    Create new user.
    """
    user = await curd.get_user_by_email(session=session, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system.",
        )

    user = curd.create_user(session=session, user_create=user_in)
    if settings.emails_enabled and user_in.email:
        email_data = generate_new_account_email(
            email_to=user_in.email, username=user_in.email, password=user_in.password
        )
        send_email(
            email_to=user_in.email,
            subject=email_data.subject,
            html_content=email_data.html_content,
        )
    return user


@router.patch("/me", response_model=UserPublic)
async def update_user_me(
    *, session: SessionDep, user_in: UserUpdateMe, current_user: CurrentUser
) -> Any:
    """Update own user."""
    if user_in.email:
        existing_user = await curd.get_user_by_email(
            session=session, email=user_in.email
        )
        if existing_user and existing_user.id != current_user.id:
            raise HTTPException(
                status_code=409, detail="User with this email already exists"
            )
    user_data = user_in.model_dump(exclude_unset=True)
    current_user.sqlmodel_update(user_data)
    session.add(current_user)
    session.commit()
    session.refresh(current_user)
    return current_user


@router.patch("/me/password", response_model=Message)
def update_password_me(
    *, session: SessionDep, body: UpdatePassword, current_user: CurrentUser
) -> Any:
    """
    Update own password.
    """
    if not verify_password(body.current_password, current_user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect password")
    if body.current_password == body.new_password:
        raise HTTPException(
            status_code=400, detail="New password cannot be the same as the current one"
        )
    hashed_password = get_password_hash(body.new_password)
    current_user.hashed_password = hashed_password
    session.add(current_user)
    session.commit()
    return Message(message="Password updated successfully")


@router.get("/me", response_model=UserPublic | None)
async def read_user_me(db: SessionDep, user: OptionalUserDep):
    """
    Get current user.
    """
    # response = UserPublic(**user.model_dump())
    # return response
    return user


@router.delete("/me", response_model=Message)
async def delete_user_me(db: SessionDep, current_user: CurrentUser) -> Any:
    """
    Delete own user.
    """
    if current_user.is_superuser:
        raise HTTPException(
            status_code=403, detail="Super users are not allowed to delete themselves"
        )
    statement = delete(Item).where(col(Item.owner_id) == current_user.id)
    db.exec(statement)  # type: ignore
    db.delete(current_user)
    db.commit()
    return Message(message="User deleted successfully")


@router.post("/signup", response_model=UserPublic)
async def register_user(session: SessionDep, user_in: UserRegister) -> Any:
    """
    Create new user without the need to be logged in.
    """
    return await curd.register_user(session=session, user_in=user_in)


@router.get("/avatar", include_in_schema=False)
async def avatar(db: SessionDep, user: OptionalUserDep):
    """
    获取用户头像
    """
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    account = get_account_by_user_id(session=db, owner_id=user.id)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")

    github_user_data = await get_github_user_data(account.token)
    if not github_user_data:
        raise HTTPException(status_code=404, detail="GitHub user data not found")

    avatar_url = github_user_data.get("avatar_url")
    if not avatar_url:
        LOG.info(f"找不到 用户头像 {github_user_data}")
        LOG.info(f"account {account}")
        raise HTTPException(status_code=404, detail="Avatar URL not found")

    async with httpx.AsyncClient() as client:
        avatar_response = await client.get(avatar_url)
        if avatar_response.status_code != 200:
            raise HTTPException(status_code=404, detail="Failed to fetch avatar")
    return Response(
        content=avatar_response.content,
        media_type=avatar_response.headers.get("content-type"),
        headers={"Cache-Control": "public, max-age=3600"},
    )


@router.get("/{user_id}", response_model=UserPublic)
def read_user_by_id(
    user_id: str,
    session: SessionDep,
    current_user: CurrentUser,
) -> Any:
    """
    Get a specific user by id.
    """
    user = session.get(User, user_id)
    if user == current_user:
        return user
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=403,
            detail="The user doesn't have enough privileges",
        )
    return user


@router.patch(
    "/{user_id}",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=UserPublic,
)
async def update_user(
    *,
    session: SessionDep,
    user_id: str,
    user_in: UserUpdate,
) -> Any:
    """
    Update a user.
    """
    db_user = session.get(User, user_id)
    if not db_user:
        raise HTTPException(
            status_code=404,
            detail="The user with this id does not exist in the system",
        )
    if user_in.email:
        existing_user = await curd.get_user_by_email(
            session=session, email=user_in.email
        )
        if existing_user and existing_user.id != user_id:
            raise HTTPException(
                status_code=409, detail="User with this email already exists"
            )

    db_user = curd.update_user(session=session, db_user=db_user, user_in=user_in)
    return db_user


@router.delete("/{user_id}", dependencies=[Depends(get_current_active_superuser)])
def delete_user(
    session: SessionDep, current_user: CurrentUser, user_id: str
) -> Message:
    """
    Delete a user.
    """
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user == current_user:
        raise HTTPException(
            status_code=403, detail="Super users are not allowed to delete themselves"
        )
    statement = delete(Item).where(col(Item.owner_id) == user_id)
    session.exec(statement)  # type: ignore
    session.delete(user)
    session.commit()
    return Message(message="User deleted successfully")
