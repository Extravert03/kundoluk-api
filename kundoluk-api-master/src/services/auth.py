from datetime import datetime, timedelta

import jwt
from fastapi import HTTPException, status, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

import settings

__all__ = ('AuthHandler',)


class AuthHandler:
    security = HTTPBearer()
    secret = settings.SECRET_KEY

    def encode_token(self, cookies: dict) -> str:
        payload_to_encode = cookies | {'exp': datetime.utcnow() + timedelta(days=1)}
        return jwt.encode(payload_to_encode, self.secret, algorithm='HS256')

    def decode_token(self, token: str) -> dict:
        try:
            payload = jwt.decode(token, self.secret, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail='Token has expired')
        except jwt.InvalidTokenError:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail='Invalid token')
        else:
            if 'exp' in payload:
                del payload['exp']
            return payload

    def auth_wrapper(self, auth: HTTPAuthorizationCredentials = Security(security)) -> dict:
        return self.decode_token(auth.credentials)
