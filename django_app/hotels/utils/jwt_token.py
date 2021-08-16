import jwt
from datetime import timedelta, datetime
import os


# create jwt token
def create_jwt_token(city):
    hotels_app_jwt_secret = os.environ.get('HOTELS_APP_JWT_SECRET_KEY')
    payload = {
        "exp": datetime.utcnow() + timedelta(hours=24),
        "city_name": city,
    }
    token = jwt.encode(payload, hotels_app_jwt_secret, algorithm="HS256")
    return {'Authorization': token}
