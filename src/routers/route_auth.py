from fastapi import APIRouter
from fastapi import Response, Request, Depends
from fastapi.encoders import jsonable_encoder
from src.schemas.schemas import UserBody, SuccessMsg, UserInfo, Csrf
from src.database.database import (
  db_signup,
  db_login,
)
from src.services.auth_utils import AuthJwtCsrf
from fastapi_csrf_protect import CsrfProtect

router = APIRouter()
auth = AuthJwtCsrf()


@router.get("/api/csrftoken", response_model=Csrf)
def get_csrf_token(csrf_protect: CsrfProtect = Depends()):
  csrf_token = csrf_protect.generate_csrf()
  res = {'csrf_token': csrf_token}
  return res


@router.post("/api/register", response_model=UserInfo)
async def signup(request: Request, user: UserBody, csrf_protect: CsrfProtect = Depends()):
  csrf_protect.validate_csrf(request)
  user = jsonable_encoder(user)
  new_user = await db_signup(user)
  return new_user


@router.post("/api/login", response_model=SuccessMsg)
async def login(request: Request, response: Response, user: UserBody, csrf_protect: CsrfProtect = Depends()):
  csrf_protect.validate_csrf(request)
  user = jsonable_encoder(user)
  token = await db_login(user)
  response.set_cookie(
    key="access_token", value=f"Bearer {token}", httponly=True,
    samesite="none", secure=True)
  return {"message": "Successfully logged in"}


@router.post("/api/logout", response_model=SuccessMsg)
async def logout(request: Request, response: Response, csrf_protect: CsrfProtect = Depends()):
  csrf_protect.validate_csrf(request)
  response.set_cookie(
    key="access_token", value="", httponly=True,
    samesite="none", secure=True
  )
  return {"message": "Successfully logged out"}


@router.post("/api/user", response_model=UserInfo)
async def get_user_refresh_jwt(request: Request, response: Response):
  new_token, subject = auth.verify_update_jwt(request)
  response.set_cookie(
    key="access_token", value=f"Bearer {new_token}", httponly=True,
    samesite="none", secure=True
  )
  return {"email": subject}
