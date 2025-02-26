import json
from dataclasses import dataclass
import os

from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from fastapi.security import APIKeyHeader
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict
from redis import Redis

authorization_header = APIKeyHeader(name="Authorization")


class MessageWithDetails(BaseModel):
    detail: str


forbidden_response = {
    403: {
        'model': MessageWithDetails,
    }
}
unauthorized_response = {
    401: {
        'model': MessageWithDetails,
        'description': 'Wrong authorization'
    }
}

access_error_response = forbidden_response | unauthorized_response

type FieldsType = str | int
type DataType = dict[str, FieldsType | DataType]


@dataclass
class AccessTokenInfo[TokenDataType: DataType]:
    user_id: str
    data: TokenDataType


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra="allow")

    redis_host: str = os.getenv('REDIS_HOST', '127.0.0.1')


class RedisAuthService[TokenDataType: DataType]:
    def __init__(self):
        self.connection = Redis(
            host=Settings().redis_host, charset="utf-8", decode_responses=True
        )

    def get_verified_info_by_access_token(
            self,
            access_token: str
    ) -> AccessTokenInfo[TokenDataType] | None:
        info = self.connection.hgetall(access_token)
        if not info:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Invalid access token'
            )
        info['data'] = json.loads(info['data'])
        return AccessTokenInfo(
            **info
        )


def _bearer_header(access_token=Depends(authorization_header)):
    if not access_token.lower().startswith('bearer'):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail='Not found Bearer'
        )
    access_token_without_bearer = access_token[7:]
    return access_token_without_bearer


class AuthService[TokenDataType: DataType]:
    def __init__(self, _: TokenDataType):
        pass

    @staticmethod
    def access(**filters):
        async def _access(
                redis_auth_service: RedisAuthService = Depends(),
                access_token=Depends(_bearer_header)
        ) -> AccessTokenInfo[TokenDataType]:
            if not access_token:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
            access_token_info = (
                redis_auth_service.get_verified_info_by_access_token(
                    access_token
                ))
            for filter_, value in filters.items():
                if access_token_info.data[filter_] != value:
                    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
            return access_token_info

        return _access
