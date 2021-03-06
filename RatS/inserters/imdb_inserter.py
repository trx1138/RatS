import re
import time

from bs4 import BeautifulSoup

from RatS.inserters.base_inserter import Inserter
from RatS.sites.imdb_site import IMDB


class IMDBRatingsInserter(Inserter):
    def __init__(self, args):
        super(IMDBRatingsInserter, self).__init__(IMDB(), args)

    def _find_movie(self, movie):
        self.site.browser.get('http://www.imdb.com/find?s=tt&ref_=fn_al_tt_mr&q=%s' % movie['title'])
        time.sleep(1)
        search_result_page = BeautifulSoup(self.site.browser.page_source, 'html.parser')
        search_results_list = search_result_page.find(class_='findList')
        if search_results_list:  # found something
            search_results = search_results_list.find_all(class_='findResult')
            for search_result in search_results:
                if self._is_requested_movie(movie, search_result):
                    return "http://www.imdb.com" + search_result.find('a')['href']
            return None
        return None

    def _is_requested_movie(self, movie, search_result):
        result_annotation = search_result.find(class_='result_text').get_text()
        result_year_list = re.findall(r'\((\d{4})\)', result_annotation)
        if len(result_year_list) > 0:
            result_year = result_year_list[-1]
            return int(result_year) == movie['year']
        return False

    def _click_rating(self, my_rating):
        self.site.browser.find_element_by_class_name('star-rating-button').find_element_by_tag_name('button').click()
        time.sleep(0.5)
        stars = self.site.browser.find_element_by_class_name('star-rating-stars').find_elements_by_tag_name('a')
        star_index = int(my_rating) - 1
        stars[star_index].click()
