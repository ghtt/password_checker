import argparse
import hashlib
import requests
from collections import Counter

URL = "https://api.pwnedpasswords.com/range/"


def get_agrs():
    argparser = argparse.ArgumentParser()
    argparser.add_argument(
        'passwords',
        nargs='*',
        type=str)
    return argparser.parse_args().passwords


def get_hash(password):
    hashed = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    return hashed[:5], hashed[5:]


def check_password(password):
    hash_password, tail = get_hash(password)
    hash_list = requests.get(URL + hash_password[:5]).text.splitlines()
    hash_list = (item.split(":") for item in hash_list)
    for h, count in hash_list:
        if h == tail:
            print(f"{h}=={tail} and counter={count}")
            return True
    return False


if __name__ == "__main__":
    passwords = get_agrs()
    for password in passwords:
        if not check_password(password):
            print(f"{password} is not found")
