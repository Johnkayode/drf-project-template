import random
import string

def generate_public_id(length: int = 10) -> str:
    letters = string.ascii_letters
    random_string = ''.join(random.choice(letters) for i in range(length))
    return random_string.lower()