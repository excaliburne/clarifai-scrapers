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
        data = None
        ) -> str:
        """
        Build a string for requested endpoint and feeds ids to pre-formatted string

        Args:
            endpoint_name (str)
            data (dict, optional): Url ids should be passed in a dict like {'user_id': 'xyz'}. Defaults to None.

        Returns:
            (str): Url
        """

        url = endpoint

        if (data):
            data = delete_none_values(data)
            url  = getattr(url, 'format')(**data)

        return url