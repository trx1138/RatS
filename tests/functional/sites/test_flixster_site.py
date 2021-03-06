from unittest import TestCase
from unittest import skip

from RatS.sites.flixster_site import Flixster


@skip('this test is unstable on travis')
class FlixsterSiteTest(TestCase):
    def setUp(self):
        self.site = Flixster()

    def test_login(self):
        self.assertIn(self.site.USERNAME, self.site.browser.page_source)

    def tearDown(self):
        self.site.kill_browser()
