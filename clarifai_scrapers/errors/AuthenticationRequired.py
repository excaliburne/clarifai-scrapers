class AuthenticationRequired(Exception):
    def __init__(self, message, code = 403):
        super().__init__(f'{message}, HTTP: {code}')