# -*- coding: utf-8 -*-

# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

# pylint: disable=missing-docstring

from __future__ import absolute_import, division, print_function, unicode_literals
import unittest

from resources.lib import CHANNELS, favorites, vrtapihelper
import addon

xbmc = __import__('xbmc')
xbmcaddon = __import__('xbmcaddon')
xbmcgui = __import__('xbmcgui')
xbmcplugin = __import__('xbmcplugin')
xbmcvfs = __import__('xbmcvfs')


class ApiHelperTests(unittest.TestCase):

    _favorites = favorites.Favorites(addon.kodi)
    _apihelper = vrtapihelper.VRTApiHelper(addon.kodi, _favorites)

    def test_get_api_data_single_season(self):
        title_items, sort, ascending, content = self._apihelper.get_episode_items(program='het-journaal')
        self.assertTrue(120 <= len(title_items) <= 140, 'We got %s items instead.' % len(title_items))
        self.assertEqual(sort, 'dateadded')
        self.assertFalse(ascending)
        self.assertEqual(content, 'episodes')

    def test_get_api_data_multiple_seasons(self):
        title_items, sort, ascending, content = self._apihelper.get_episode_items(program='thuis')
        self.assertTrue(len(title_items) < 5)
        self.assertEqual(sort, 'label')
        self.assertFalse(ascending)
        self.assertEqual(content, 'seasons')

    def test_get_api_data_specific_season(self):
        title_items, sort, ascending, content = self._apihelper.get_episode_items(program='pano')
        self.assertEqual(len(title_items), 4)
        self.assertEqual(sort, 'label')
        self.assertFalse(ascending)
        self.assertEqual(content, 'seasons')

    def test_get_api_data_specific_season_without_broadcastdate(self):
        title_items, sort, ascending, content = self._apihelper.get_episode_items(program='postbus-x')
        self.assertEqual(len(title_items), 3)
        self.assertEqual(sort, 'label')
        self.assertTrue(ascending)
        self.assertEqual(content, 'seasons')

    def test_get_recent_episodes(self):
        ''' Test items, sort and order '''
        episode_items, sort, ascending, content = self._apihelper.get_episode_items(page=1, variety='recent')
        self.assertEqual(len(episode_items), 50)
        self.assertEqual(sort, 'dateadded')
        self.assertFalse(ascending)
        self.assertEqual(content, 'episodes')

    def test_get_recent_episodes_page1(self):
        ''' Test items, sort and order '''
        episode_items, sort, ascending, content = self._apihelper.get_episode_items(page=2, variety='recent')
        self.assertEqual(len(episode_items), 50)
        self.assertEqual(sort, 'dateadded')
        self.assertFalse(ascending)
        self.assertEqual(content, 'episodes')

    def test_get_recent_episodes_page2(self):
        ''' Test items, sort and order '''
        episode_items, sort, ascending, content = self._apihelper.get_episode_items(page=3, variety='recent')
        self.assertEqual(len(episode_items), 50)
        self.assertEqual(sort, 'dateadded')
        self.assertFalse(ascending)
        self.assertEqual(content, 'episodes')

    def test_get_offline_episodes(self):
        ''' Test items, sort and order '''
        episode_items, sort, ascending, content = self._apihelper.get_episode_items(page=1, variety='offline')
        self.assertTrue(episode_items)
        self.assertEqual(sort, 'dateadded')
        self.assertFalse(ascending)
        self.assertEqual(content, 'episodes')

    def test_get_tvshows(self):
        ''' Test items, sort and order '''
        category = 'nieuws-en-actua'
        tvshow_items = self._apihelper.get_tvshow_items(category=category)
        self.assertTrue(tvshow_items)

    def test_tvshows(self):
        ''' Test A-Z tvshow listing and CHANNELS list '''
        tvshow_items = self._apihelper.get_tvshow_items(category=None)

        # Test we get a non-empty A-Z listing back
        self.assertTrue(tvshow_items)

        # Test every brand is a known channel studio name
        bogus_brands = ['lang-zullen-we-lezen', 'VRT']
        channel_studios = [c.get('studio') for c in CHANNELS] + bogus_brands
        for tvshow in tvshow_items:
            self.assertTrue(tvshow.info_dict['studio'] in channel_studios, '%s | %s | %s' % (tvshow.title, tvshow.info_dict['studio'], channel_studios))

    def test_get_latest_episode(self):
        video = self._apihelper.get_latest_episode(program='het-journaal')
        self.assertTrue(len(video) == 2)
        self.assertTrue(video.get('video_id') is not None)
        self.assertTrue(video.get('publication_id') is not None)


if __name__ == '__main__':
    unittest.main()
