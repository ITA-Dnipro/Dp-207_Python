import jwt
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()


def create_jwt_token(payload):
    '''
    Return JWT token encoded with .env file sekret
    '''
    TRANSPORT_APP_JWT_SECRET = os.environ.get('TRANSPORT_APP_JWT_SECRET')
    #
    incoming_date = dict(payload)
    incoming_date['exp'] = datetime.utcnow() + timedelta(seconds=300)
    #
    token = jwt.encode(
        incoming_date,
        TRANSPORT_APP_JWT_SECRET,
        algorithm="HS256"
    )
    return token
