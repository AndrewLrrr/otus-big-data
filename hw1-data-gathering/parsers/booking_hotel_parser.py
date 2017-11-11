import re

from parsers.parser import Parser


class BookingHotelParser(Parser):
    def title(self):
        item = self._soup.find('h2', {'id': 'hp_hotel_name'})
        if item:
            return item.text.replace('\n', '')
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
        item = self._soup.find('div', {'id': 'reviewFloater'})
        if item:
            rating = item.find('span', {'class': 'review-score-badge'})
            if rating:
                return float(rating.text.replace(',', '.'))
        return None

    def reviews_count(self):
        item = self._soup.find('div', {'id': 'reviewFloater'})
        if item:
            reviews_count = item.find('span', {'class': 'review-score-widget__subtext'})
            if reviews_count:
                return int(re.sub('[^\d]+', '', reviews_count.text))
        return None

    def the_year_of_the_beginning_on_the_booking(self):
        item = self._soup.find('p', {'class': 'hotel_meta_style'})
        if item:
            search = re.search('.*(\d\d\d\d)\.', item.text, re.IGNORECASE)
            if search:
                return int(search.group(1))
        return None

    def has_free_wifi(self):
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

    def address(self):
        item = self._soup.find('span', {'class': 'hp_address_subtitle'})
        if item:
            return item.text.replace('\n', '')
        return None

    def hotel_summary(self):
        item = self._soup.find('div', {'id': 'summary'})
        if item:
            ps = item.find_all('p', {'class': None})
            if ps:
                del ps[0]
                return ' '.join([p.text.replace('\n', '').strip() for p in ps])
        return None

    def district_summary(self):
        ps = self._soup.find_all('p', {'class': 'hp_district_endorsements'})
        if ps:
            return ' '.join([p.text.replace('\n', '').strip() for p in ps])
        return None

    def reviews_summary(self):
        ps = self._soup.find_all('p', {'class': 'hp-desc-review-highlight'})
        if ps:
            return ' '.join([p.text.replace('\n', '').strip() for p in ps])
        return None

    def geo_summary(self):
        ps = self._soup.find_all('p', {'class': 'geo_information'})
        if ps:
            return ' '.join([p.text.replace('\n', '').strip() for p in ps])
        return None
