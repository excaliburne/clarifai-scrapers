class FailedAuthentication(Exception):
    def __init__(self, service, code = 401):
        super().__init__(f'Failed to authenticate: {service}, HTTP: {code}')