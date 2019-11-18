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


def hash_password(password):
    return [hashlib.sha1(password.encode('utf-8')).hexdigest().upper()]


def check_password(password):
    hash_list = requests.get(URL + password[:5]).text.split("\r\n")
    return [item[:item.index(":")] for item in hash_list]


if __name__ == "__main__":
    passwords = get_agrs()
    passwords = {password: hash_password(password) for password in passwords}
    for password in passwords.keys():
        check_result = check_password(*passwords[password])
        if check_result:
            passwords[password].extend(check_result)
    for password, hash_values in passwords.items():
        if filter(lambda x: x[1] >= 2, Counter(hash_values)):
            print(f"{password} is found in database")
