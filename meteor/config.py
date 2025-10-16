import os
import secrets


class Config:
    SECRET_KEY = os.environ.get("METEOR_SECRETKEY", secrets.token_hex(32))
