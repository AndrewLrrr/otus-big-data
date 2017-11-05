from parsers.parser import Parser


class BookingCatalogParser(Parser):
    def catalog_links(self):
        links = []

        objects_list = self._soup.find_all('a', {'class': 'hotel_name_link url'})

        for link in objects_list:
            links.append('https://booking.com{}'.format(link.get('href')))

        return [l.replace('\n', '') for l in links]
