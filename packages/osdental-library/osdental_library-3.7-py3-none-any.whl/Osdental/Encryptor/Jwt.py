import jwt
from Osdental.Exception.ControlledException import JWTokenException
from Osdental.Utils.Message import UNEXPECTED_ERROR
from Osdental.Utils.Code import APP_ERROR

class JWT:

    @staticmethod
    def generate_token(payload: dict, jwt_secret_key:str) -> str:
        try:
            token = jwt.encode(payload, jwt_secret_key, algorithm='HS256')
            return token

        except Exception as e:
            raise JWTokenException(message=UNEXPECTED_ERROR, error=str(e), status_code=APP_ERROR)


    @staticmethod
    def extract_payload(jwt_token: str, jwt_secret_key:str) -> dict:
        try:
            payload = jwt.decode(jwt_token, jwt_secret_key, algorithms=['HS256'])
            return payload

        except Exception as e:
            raise JWTokenException(message=UNEXPECTED_ERROR, error=str(e), status_code=APP_ERROR) 