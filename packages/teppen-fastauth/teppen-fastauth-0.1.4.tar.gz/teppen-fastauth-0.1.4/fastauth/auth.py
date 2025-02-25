from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jwt.exceptions import (
    InvalidSignatureError,
    ExpiredSignatureError,
    PyJWKSetError,
    InvalidAudienceError,
    PyJWKClientConnectionError,
    PyJWKClientError,
)

from .decode import decode_access_token_using_jwks
from .exceptions import NoTokenException


def get_bearer_access_token_decode(
    authorization: HTTPAuthorizationCredentials = Depends(HTTPBearer(auto_error=False)),
):
    if authorization is None:
        raise HTTPException(401, "トークンがありません。")

    try:
        token = authorization.credentials
        return decode_access_token_using_jwks(token)
    except InvalidSignatureError:
        raise HTTPException(400, "署名が不正です。")
    except ExpiredSignatureError:
        raise HTTPException(401, "トークンの期限が切れています。")
    except InvalidAudienceError:
        raise HTTPException(400, "InvalidAudienceError: aud が不正です。")
    except PyJWKSetError as e:
        raise HTTPException(
            401, "JWKSエンドポイントから鍵セットを取得できませんでした。"
        )
    except NoTokenException:
        raise HTTPException(401, "トークンがありません。")
    except PyJWKClientConnectionError as e:
        raise HTTPException(
            500,
            "JWKSエンドポイントに接続できませんでした。バックエンドアプリのProxy設定を解除してみて下さい。",
        )
    except PyJWKClientError as e:
        raise HTTPException(401, "JWKSエンドポイントに対象の鍵が存在しませんでした。")
    except Exception as e:
        print(e)
        raise HTTPException(500, "予期せぬエラーが発生しました。")
