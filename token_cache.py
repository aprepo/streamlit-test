import os


class TokenCache(object):
    def __init__(self, filename):
        self.filename = filename

    def get_token(self):
        try:
            f = open(self.filename, "r")
            token = f.read()
            f.close()
            return token
        except FileNotFoundError as e:
            return None

    def put_token(self, token):
        f = open(self.filename, "w")
        f.write(token)
        f.close()

    def clear_cache(self):
        try:
            os.remove(self.filename)
        except FileNotFoundError as e:
            pass
