import secrets
import random
import string
import bcrypt


alphabet = string.ascii_letters + string.digits

def generate_password(password_length: int = 13) -> str:
    """
    Generate a password of a certain length using the argument, default is 13
    """
    return ''.join(random.choice(alphabet) for i in range(password_length))

def generate_hashed_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashcode = bcrypt.hashpw(
        password=password.encode(encoding='utf-8'),
        salt=salt
        ).decode(encoding='utf-8')
    return hashcode

def validate_password(hashed_password: str, password: str) -> bool:
    check_status = bcrypt.checkpw(
        password=password.encode(encoding='utf-8'),
        hashed_password=hashed_password.encode(encoding='utf-8')
        )
    return check_status

