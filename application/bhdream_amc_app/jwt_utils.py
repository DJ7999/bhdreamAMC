# BHDREAM_AMC_APP/jwt_utils.py
import jwt
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from django.conf import settings

def generate_jwt_token(user):
    expiration_time = datetime.utcnow() + timedelta(days=1)
    payload = {
        'user_id': user.id,
        'exp': expiration_time,
        'iat': datetime.utcnow(),
        'is_active': user.is_active,
        'is_staff': user.is_staff,
    }
    secret_key = settings.SECRET_KEY
    token = jwt.encode(payload, secret_key, algorithm='HS256')
    return token

def decode_jwt_token(token):
    secret_key = settings.SECRET_KEY
    try:
        decoded_token = jwt.decode(token, secret_key, algorithms=["HS256"])
        return decoded_token
    except jwt.ExpiredSignatureError:
        print("Token has expired")
        return None
    except jwt.InvalidTokenError:
        print("Invalid token")
        return None
