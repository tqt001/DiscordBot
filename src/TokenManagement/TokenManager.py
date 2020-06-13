class TokenManager(object):

    def __init__(self, token_dir):
        self.token_dir = token_dir

    def read_token(self):
        with open(self.token_dir, "r") as f:
            lines = f.readlines()
            return lines[0].strip()