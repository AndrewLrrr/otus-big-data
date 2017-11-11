import requests

from decorators.decorators import retry


class Scrapper:
    _headers = {
        'User-Agent': 'Hello my name is AI bot and I need some data from you:)'
    }

    def __init__(self):
        self.timeout = 3

    @retry(requests.RequestException)
    def _do_request(self, url, params=None, proxy=None, secure=True):
        protocol = 'https' if secure else 'http'

        response = requests.get(
            url,
            params=params,
            headers=self._headers,
            timeout=self.timeout,
            proxies={protocol: proxy}
        )

        response.raise_for_status()

        return response.text
