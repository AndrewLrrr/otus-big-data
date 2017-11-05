import requests
from requests import RequestException

from decorators.decorators import retry
from parsers.proxy_list_parser import ProxyListParser


class Proxy:
    _url = 'https://www.ip-adress.com/proxy-list'
    _headers = {
        'Hello my name is AI bot and I need some proxy from you:)'
    }

    def __init__(self):
        self._except = set()
        self.timeout = 3

    def get_proxy(self):
        data = self._do_request(self._url)
        parser = ProxyListParser()
        ips = parser.get_proxy_ips(data)
        for ip in ips:
            url = 'http://{}'.format(ip)
            if url in self._except:
                continue
            try:
                self._do_request('https://ya.ru', proxy=url)
                return url
            except requests.ConnectionError:
                continue
        return None

    def forget_proxy(self, url):
        self._except.add(url)

    @retry(RequestException)
    def _do_request(self, url, params=None, proxy=None):
        response = requests.get(url, params=params, timeout=self.timeout, proxies={'https': proxy})

        response.raise_for_status()

        return response.text
