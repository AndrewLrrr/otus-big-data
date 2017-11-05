from bs4 import BeautifulSoup


class ProxyListParser:
    def get_proxy_ips(self, data):
        """
        Parses html text and extracts field values
        :param data: html text (page)
        :return: a dictionary where key is one
        of defined fields and value is this field's value
        """
        soup = BeautifulSoup(data, 'html.parser')
        ips = []

        objects_list = soup.find('table', {'class': 'proxylist'})

        for tr in objects_list.find('tbody').find_all('tr'):
            item = tr.find_all('td')[0]
            ips.append(item.text)

        return ips
