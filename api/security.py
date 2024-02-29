from datetime import datetime, timedelta
from jose import jwt, ExpiredSignatureError

secret_key = '541faf5284a993e6409c749c24dce5ad6dc9bd79a8e4fa672289801c4d14cfae'


def create_access_token(username: str) -> str:
    expires = datetime.utcnow() + timedelta(hours=6)
    to_encode = {'status_code': 200, 'exp': expires, 'username': username}

    return jwt.encode(to_encode, secret_key, algorithm='HS256')


def decode_access_token(access_token: str):
    try:
        return jwt.decode(access_token, secret_key, algorithms='HS256')
    except ExpiredSignatureError:
        # 令牌过期
        return {'status_code': 500, 'msg': 'token expires.'}
    except Exception as other_error:
        print(other_error)
        return {'status_code': 500, 'msg': 'unknown error.'}
