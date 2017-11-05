from bs4 import BeautifulSoup


class BookingCatalogParser:
    def get_catalog_links(self, data):
        """
        Parses html text and extracts field values
        :param data: html text (page)
        :return: a dictionary where key is one
        of defined fields and value is this field's value
        """
        soup = BeautifulSoup(data, 'html.parser')
        links = []

        objects_list = soup.find_all('a', {'class': 'hotel_name_link url'})

        for link in objects_list:
            links.append('https://booking.com{}'.format(link.get('href')))

        return [l.replace('\n', '') for l in links]
