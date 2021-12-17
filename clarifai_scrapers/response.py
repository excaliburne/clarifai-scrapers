# UTILS
from clarifai_scrapers.utils.decorators import add_all_args_to_self

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


    def __call__(self, **kwargs):
        return self.returns(**kwargs)

    
    def _template(self):
        return {
            'total': len(list(self.results)),
            'results': self.results,
            **self.additional_data
        }
    
    
    @add_all_args_to_self
    def returns(
        self,
        results: list, 
        additional_data: dict = {}
        ):
        
        return self._template()
