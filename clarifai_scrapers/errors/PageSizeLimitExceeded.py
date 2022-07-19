class PageSizeLimitExceeded(Exception):
    def __init__(self, details):
        super().__init__(f'Page size exceed limit: {details}')