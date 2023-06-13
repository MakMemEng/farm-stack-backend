from fastapi import APIRouter
from fastapi import Response, Request, Depends
from fastapi.encoders import jsonable_encoder
from src.schemas import UserBody, SuccessMsg, UserInfo
from src.database import (
  db_signup,
  db_login,
)
from src.auth_utils import AuthJwtCsrf

router = APIRouter()
auth = AuthJwtCsrf()


@router.post("/api/register", response_model=UserInfo)
async def signup(user: UserBody):
  user = jsonable_encoder(user)
  new_user = await db_signup(user)
  return new_user


@router.post("/api/login", response_model=SuccessMsg)
async def login(user: UserBody):
  user = jsonable_encoder(user)
  token = await db_login(user)
  return {"message": "Successfully logged in"}


