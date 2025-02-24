import jwt
from .model import AccessTokenPayload
from .env import JWT_ALGORITHM, JWT_AUDIENCE, JWKS_ENDPOINT
from .exceptions import NoTokenException


def decode_access_token_using_jwks(token: str):
    if token is None:
        raise NoTokenException()

    jwks_client = jwt.PyJWKClient(JWKS_ENDPOINT)
    signing_key = jwks_client.get_signing_key_from_jwt(token)
    payload = jwt.decode(token, signing_key.key, algorithms=[
                         JWT_ALGORITHM], audience=JWT_AUDIENCE)

    return AccessTokenPayload(**payload)
