from .const import API_URL_PATH


def get_url_from_options(url: str) -> str:
    if url.endswith(API_URL_PATH):
        return url
    else:
        return url + API_URL_PATH
