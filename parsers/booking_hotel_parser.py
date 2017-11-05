import re

from parsers.parser import Parser


class BookingHotelParser(Parser):
    def title(self):
        item = self._soup.find('h2', {'id': 'hp_hotel_name'})
        if item:
            return item.text
        return None

    def stars(self):
        item = self._soup.find('span', {'class': 'hp__hotel_ratings__stars'})
        if item:
            stars = item.find('span', {'class': 'invisible_spoken'})
            if stars:
                search = re.search('^([\d]+)-.*', stars.text, re.IGNORECASE)
                if search:
                    return int(search.group(1))
        return None

    def rating(self):
        item = self._soup.find('span', {'class': 'review-score-badge'})
        if item:
            return float(item.text.replace(',', '.'))
        return None

    def reviews_count(self):
        item = self._soup.find('span', {'class': 'review-score-widget__subtext'})
        if item:
            return int(re.sub('[^\d]+', '', item.text))
        return None

    def the_year_of_the_beginning_on_the_booking(self):
        item = self._soup.find('p', {'class': 'hotel_meta_style'})
        if item:
            search = re.search('.*(\d\d\d\d)\.', item.text, re.IGNORECASE)
            if search:
                return int(search.group(1))
        return None

    def free_wifi(self):
        item = self._soup.find('div', {
            'class': 'important_facility',
            'data-name-en': 'Free WiFi Internet Access Included'
        })
        return True if item else False

    def gallery_images(self):
        images = []
        items = self._soup.find_all('img')
        if items:
            for item in items:
                image = item.get('src')
                if image and image.find('/images/hotel/') != -1:
                    images.append(image)
        return images
