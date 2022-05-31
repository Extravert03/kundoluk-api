from fastapi import APIRouter, status

from schemas import AuthCredentials, GeneratedToken
from services import kundoluk
from services.auth import AuthHandler

auth_handler = AuthHandler()
router = APIRouter(
    prefix='/auth',
    tags=['Authentication tools'],
)


@router.post(
    path='/token/generate',
    status_code=status.HTTP_201_CREATED,
    response_model=GeneratedToken,
)
async def auth_in_kundoluk(auth_credentials: AuthCredentials):
    cookies = await kundoluk.get_auth_cookies(auth_credentials)
    token = auth_handler.encode_token(cookies)
    return {'token': token}
