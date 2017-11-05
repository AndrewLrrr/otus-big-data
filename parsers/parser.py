from bs4 import BeautifulSoup


class Parser:
    def __init__(self, data):
        self._soup = BeautifulSoup(data, 'html.parser')
