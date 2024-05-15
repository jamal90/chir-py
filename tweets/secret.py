import os
import base64


def cookie_secret():
    print(base64.urlsafe_b64encode(os.urandom(32)).decode())


if __name__ == '__main__':
    cookie_secret()
