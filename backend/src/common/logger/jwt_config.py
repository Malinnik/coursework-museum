import jwt
import logging
import os

from aiohttp.web import Application, HTTPUnauthorized
from datetime import datetime, timedelta, timezone

from common.db.pg_users import get_user_by_id

async def encode_access(app: Application, user_id: int, expiracy: timedelta = timedelta(minutes=30)) -> str:
    try:
        user = await get_user_by_id(app, user_id)
        payload = {
            "user": {
                'id': user.id,
                'username': user.username,
                'email': user.email,
            },
            "expiracy": str(datetime.now(tz=timezone.utc) + expiracy)
        }
        token = jwt.encode(payload, os.getenv("TOKEN_KEY"), algorithm="HS256")
        return token
    except Exception as e:
        logging.error(f"Error: {e}")


async def decode_access(app: Application, header: str, signature: bool = True) -> dict:
    try:
        bearer, token = header.split(" ")
        if bearer.find("Bearer") == -1:
            raise HTTPUnauthorized
        payload = jwt.decode(token, os.getenv("TOKEN_KEY"), algorithm="HS256", options={"verify_signature": signature})

        if signature == False:
            return payload['user']
        if payload['expiracy'] > int(datetime.now(tz=timezone.utc).timestamp()):
            raise HTTPUnauthorized
        
        return payload['user']

    except Exception as e:
        logging.error(f"Error: {e}")
        raise HTTPUnauthorized