from urllib.parse import urlencode

class RequestHelperUtil:
    @staticmethod
    def form_url_with_params(base_url: str, endpoint: str, params: dict) -> str:
        query_string = urlencode(params)
        return f"{base_url}{endpoint}?{query_string}"