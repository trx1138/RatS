import os
from unittest import TestCase
from unittest.mock import patch

from RatS.parsers.letterboxd_parser import LetterboxdRatingsParser

TESTDATA_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, 'assets'))


class LetterboxdParserTest(TestCase):

    @patch('RatS.parsers.base_parser.Parser.__init__')
    @patch('RatS.sites.base_site.Firefox')
    def test_init(self, browser_mock, base_init_mock):
        LetterboxdRatingsParser(None)

        self.assertTrue(base_init_mock.called)

    @patch('RatS.utils.file_impex.extract_file_from_archive')
    @patch('RatS.parsers.letterboxd_parser.LetterboxdRatingsParser._get_downloaded_filename')
    @patch('RatS.parsers.letterboxd_parser.LetterboxdRatingsParser._parse_movies_from_csv')
    @patch('RatS.parsers.letterboxd_parser.LetterboxdRatingsParser._rename_csv_file')
    @patch('RatS.sites.base_site.Firefox')
    @patch('RatS.parsers.base_parser.Parser.__init__')
    @patch('RatS.parsers.letterboxd_parser.Letterboxd')
    def test_parser(self, site_mock, base_init_mock, browser_mock, rename_csv_mock, parse_csv_mock,  # pylint: disable=too-many-arguments
                    parsed_filename_mock, zip_extraction_mock):
        parser = LetterboxdRatingsParser(None)
        parser.movies = []
        parser.site = site_mock
        parser.site.site_name = 'Letterboxd'
        parser.site.browser = browser_mock
        parser.exports_folder = os.path.abspath(os.path.join(TESTDATA_PATH, 'exports'))
        parser.csv_filename = '1234567890_letterboxd.csv'
        parsed_filename_mock.return_value = ['letterboxd.zip']

        parser.parse()

        self.assertEqual(1, zip_extraction_mock.call_count)
        self.assertEqual(1, rename_csv_mock.call_count)
        self.assertEqual(1, parse_csv_mock.call_count)

    @patch('RatS.sites.base_site.Firefox')
    @patch('RatS.parsers.base_parser.Parser.__init__')
    @patch('RatS.parsers.letterboxd_parser.Letterboxd')
    def test_csv_rename(self, site_mock, base_init_mock, browser_mock):  # pylint: disable=too-many-arguments
        parser = LetterboxdRatingsParser(None)
        parser.movies = []
        parser.site = site_mock
        parser.site.site_name = 'Letterboxd'
        parser.site.browser = browser_mock
        parser.exports_folder = os.path.abspath(os.path.join(TESTDATA_PATH, 'exports'))
        parser.csv_filename = '1234567890_letterboxd.csv'

        self.assertFalse(os.path.isfile(os.path.join(TESTDATA_PATH, 'exports', 'ratings.csv')))
        with open(os.path.join(TESTDATA_PATH, 'exports', 'ratings.csv'), 'w+'):
            self.assertTrue(os.path.isfile(os.path.join(TESTDATA_PATH, 'exports', 'ratings.csv')))
        self.assertFalse(os.path.isfile(os.path.join(TESTDATA_PATH, 'exports', parser.csv_filename)))

        parser._rename_csv_file()  # pylint: disable=protected-access

        self.assertFalse(os.path.isfile(os.path.join(TESTDATA_PATH, 'exports', 'ratings.csv')))
        self.assertTrue(os.path.isfile(os.path.join(TESTDATA_PATH, 'exports', parser.csv_filename)))
        os.remove(os.path.join(TESTDATA_PATH, 'exports', parser.csv_filename))

    @patch('RatS.sites.base_site.Firefox')
    @patch('RatS.parsers.base_parser.Parser.__init__')
    @patch('RatS.parsers.letterboxd_parser.Letterboxd')
    def test_parse_movies_from_csv(self, site_mock, base_init_mock, browser_mock):
        parser = LetterboxdRatingsParser(None)
        parser.movies = []
        parser.site = site_mock
        parser.site.site_name = 'Letterboxd'
        parser.site.browser = browser_mock
        parser.exports_folder = os.path.abspath(os.path.join(TESTDATA_PATH, 'exports'))
        parser.csv_filename = '1234567890_letterboxd.csv'

        movies = parser._parse_movies_from_csv(os.path.join(TESTDATA_PATH, 'my_ratings', 'letterboxd.csv'))  # pylint: disable=protected-access

        self.assertEqual(1056, len(movies))
        self.assertEqual(dict, type(movies[0]))
        self.assertEqual('Life', movies[0]['title'])
        self.assertEqual(2017, movies[0]['year'])
        self.assertEqual('https://letterboxd.com/film/life-2017/', movies[0]['letterboxd']['url'])
        self.assertEqual(7, movies[0]['letterboxd']['my_rating'])
