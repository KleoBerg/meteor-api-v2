import os
import secrets

class Config:
    SECRET_KEY = os.environ.get('METEOR_SECRETKEY', secrets.token_hex(32))
    DGRAPH_HOST = os.environ.get('DGRAPH_HOST', 'localhost')
    DGRAPH_PORT = os.environ.get('DGRAPH_PORT', '9080')