from common_utils_pkg.types import AccessToken, RefreshToken, BasicJWTToken
import time
import jwt
import bcrypt


def decode_access_token(token: str, secret: str) -> AccessToken:
    return AccessToken.model_validate(jwt.decode(token, secret, algorithms=["HS256"]))


def decode_refresh_token(token: str, secret: str) -> RefreshToken:
    return RefreshToken.model_validate(jwt.decode(token, secret, algorithms=["HS256"]))


def create_access_token(
    issuer: str, subject: str, duration_sec: int, roles: list[str], secret: str
) -> str:
    now = int(time.time())
    payload = AccessToken(
        iss=issuer,
        sub=subject,
        iat=now,
        exp=now + duration_sec,
        roles=roles,
    )
    return jwt.encode(payload.model_dump(), secret, algorithm="HS256")


def create_refresh_token(issuer: str, subject: str, duration_sec: int, refresh_secret: str) -> str:
    now = int(time.time())
    payload = RefreshToken(
        iss=issuer,
        sub=subject,
        iat=now,
        exp=now + duration_sec,
    )
    return jwt.encode(payload.model_dump(), refresh_secret, algorithm="HS256")


def is_token_valid(token: BasicJWTToken):
    now = int(time.time())
    is_valid = now > token.iat and now < token.exp
    return is_valid


def token_has_role(token: AccessToken, role: str) -> bool:
    return role in token.roles


def hash_password(password: str) -> bytes:
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed_password


def check_password(stored_password: str, provided_password: str) -> bool:
    return bcrypt.checkpw(provided_password.encode("utf-8"), stored_password.encode("utf-8"))
