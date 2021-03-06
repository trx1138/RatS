from unittest import TestCase
from unittest import skip

from RatS.sites.letterboxd_site import Letterboxd


@skip('this test is unstable on travis')
class LetterboxdSiteTest(TestCase):
    def setUp(self):
        self.site = Letterboxd()

    def test_login(self):
        self.assertIn(self.site.USERNAME, self.site.browser.page_source)

    def tearDown(self):
        self.site.kill_browser()
