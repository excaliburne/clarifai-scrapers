class FailedAuthentication(Exception):
    def __init__(self, service: str, description: str, http_code: int = 401):
        super().__init__(f'Failed to authenticate: {service}, {description}, HTTP: {http_code}')

        self.service     = service
        self.description = description
        self.http_code   = http_code


    def __repr__(self) -> str:
        return super().__repr__(f'Failed to authenticate: {self.service}, HTTP: {self.http_code}')