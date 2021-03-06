from unittest import TestCase
from unittest import skip

from RatS.sites.criticker_site import Criticker


@skip('this test is unstable on travis')
class CritickerSiteTest(TestCase):
    def setUp(self):
        self.site = Criticker()

    def test_login(self):
        self.assertIn(self.site.USERNAME, self.site.browser.page_source)

    def tearDown(self):
        self.site.kill_browser()
