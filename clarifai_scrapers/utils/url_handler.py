# UTILS
from clarifai_scrapers.utils.dicts import delete_none_values


class UrlHandler:
    """
    All utils related to building and manipulating urls
    """

    @classmethod
    def build(
        cls, 
        endpoint: str,
        path_variables: dict = None,
        query_params: dict = None
        ) -> str:
        """
        Build a string for requested endpoint and feeds ids to pre-formatted string

        Args:
            endpoint (str)
            path_variables (dict, optional): Url ids should be passed in a dict like {'user_id': 'xyz'}. Defaults to None.
            query_params (dict, optional)

        Returns:
            (String)
        """

        url               = endpoint
        query_params_list = []

        if (path_variables):
            url = getattr(endpoint, 'format')(**delete_none_values(path_variables))
        
        if query_params:
            for idx, query_param in enumerate(query_params.items()):
                if query_param[1] is not None:
                    if idx == 0:
                        query = f'?{query_param[0]}={query_param[1]}'
                    else:
                        query = f'&{query_param[0]}={query_param[1]}'
                    
                    query_params_list.append(query)

        return url + ''.join(query_params_list)
