

class Response:
    """
    Package response object entry point
    """

    def __init__(self):
        self.search = SearchResults()


class SearchResults:
    """
    Specifically focuses on returning search results
    """
    def __init__(self):
        self.results = []
        self.additional_data = {}


    def __call__(self, *args):
        return self.returns(*args)

    
    def _template(self):
        return {
            'total': len(list(self.results)),
            'results': self.results,
            **self.additional_data
        }
    
    
    def returns(
        self,
        results: list, 
        additional_data: dict = {}
        ):
        for param in list(locals().items())[1:]:
            setattr(self, param[0], param[1])

        return self._template()
