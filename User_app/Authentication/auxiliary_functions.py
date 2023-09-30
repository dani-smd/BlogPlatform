import json
import random
from redis import Redis
from requests import request
# --- Reading from .env file
from environs import Env

env = Env()
env.read_env()
# --- Redis Connection
redis_connection = Redis(host=env('REDIS_HOST'), port=env('REDIS_PORT'), decode_responses=True)
# --- Sending Messages
VERIFICATION_DOMAIN = f"https://api.kavenegar.com/v1/{env('API_KEY')}/verify/lookup.json"


def generate_random_token() -> str:
    try:
        token = random.randint(10000, 99999)
        if len(str(token)) != 5:
            generate_random_token()
        return str(token)
    except Exception as e:
        return f"error: {str(e)}"


def add_dict_to_redis(key: str, value: [dict, list], *args, **kwargs) -> bool:
    try:
        return redis_connection.set(key, json.dumps(value), **kwargs)
    except:
        return False


def get_dict_from_redis(key: str) -> dict:
    try:
        return {'status': True, "data": json.loads(redis_connection.get(key))}
    except:
        return {'status': False, "data": None}


def delete_item_from_redis(key: str) -> bool:
    try:
        return bool(redis_connection.delete(key))
    except:
        return False


def send_message(phone_number: str, token_1: str, token_2: str, token_3: str = "login") -> bool:
    try:
        template_name = "RegistrationNotification"
        params = f"receptor={phone_number}&token10={token_1}&token20={token_2}&token={token_3}&template={template_name}"
        # ---
        url = f"{VERIFICATION_DOMAIN}?{params}"
        req = request("GET", url)
        if req.status_code == 200:
            return True
        return False
    except:
        return False
