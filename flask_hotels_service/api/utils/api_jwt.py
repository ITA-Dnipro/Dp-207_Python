import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidSignatureError, DecodeError
from dotenv import load_dotenv
import os


load_dotenv()

# token validation
def check_token(token):
    jwt_secret = os.environ.get('HOTELS_APP_JWT_SECRET_KEY')
    print(jwt_secret)
    try:
        jwt.decode(
            token,
            'hotels_env_secret_key',
            algorithms=["HS256"]
        )
        return True
    except (
            InvalidSignatureError,
            ExpiredSignatureError,
            DecodeError
    ):
        return False