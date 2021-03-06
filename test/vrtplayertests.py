# -*- coding: utf-8 -*-

# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

# pylint: disable=missing-docstring

from __future__ import absolute_import, division, print_function, unicode_literals
import random
import unittest

from resources.lib import CATEGORIES, favorites, vrtapihelper, vrtplayer
import addon

xbmc = __import__('xbmc')
xbmcaddon = __import__('xbmcaddon')
xbmcgui = __import__('xbmcgui')
xbmcplugin = __import__('xbmcplugin')
xbmcvfs = __import__('xbmcvfs')


class TestVRTPlayer(unittest.TestCase):

    _favorites = favorites.Favorites(addon.kodi)
    _apihelper = vrtapihelper.VRTApiHelper(addon.kodi, _favorites)
    _vrtplayer = vrtplayer.VRTPlayer(addon.kodi)

    def test_show_videos_single_episode_shows_videos(self):
        program = 'marathonradio'
        episode_items, sort, ascending, content = self._apihelper.get_episode_items(program=program)
        self.assertTrue(episode_items, msg=program)
        self.assertEqual(sort, 'dateadded')
        self.assertFalse(ascending)
        self.assertEqual(content, 'episodes')

        self._vrtplayer.show_episodes(program)
        # self.assertTrue(self._kodi.show_listing.called)

    def test_show_videos_single_season_shows_videos(self):
        program = 'het-weer'
        episode_items, sort, ascending, content = self._apihelper.get_episode_items(program=program)
        self.assertTrue(episode_items, msg=program)
        self.assertEqual(sort, 'dateadded')
        self.assertFalse(ascending)
        self.assertEqual(content, 'episodes')

        self._vrtplayer.show_episodes(program)
        # self.assertTrue(self._kodi.show_listing.called)

    def test_show_videos_multiple_seasons_shows_videos(self):
        program = 'pano'
        episode_items, sort, ascending, content = self._apihelper.get_episode_items(program=program)
        self.assertTrue(episode_items)
        self.assertEqual(sort, 'label')
        self.assertFalse(ascending)
        self.assertEqual(content, 'seasons')

        self._vrtplayer.show_episodes(program)
        # self.assertTrue(self._kodi.show_listing.called)

    def test_show_videos_specific_seasons_shows_videos(self):
        program = 'thuis'
        episode_items, sort, ascending, content = self._apihelper.get_episode_items(program=program)
        self.assertTrue(episode_items, msg=program)
        self.assertEqual(sort, 'label')
        self.assertFalse(ascending)
        self.assertEqual(content, 'seasons')

        self._vrtplayer.show_episodes(program)
        # self.assertTrue(self._kodi.show_listing.called)

    def test_categories_scraping(self):
        ''' Test to ensure our hardcoded categories conforms to scraped categories '''
        # Remove thumbnails from scraped categories first
        categories_scraped = [dict(id=c['id'], name=c['name']) for c in self._apihelper.get_categories()]
        categories_stored = [dict(id=c['id'], name=c['name']) for c in CATEGORIES]
        self.assertEqual(categories_scraped, categories_stored)

    def test_random_tvshow_episodes(self):
        ''' Rest episode from a random tvshow in a random category '''
        categories = self._apihelper.get_categories()
        self.assertTrue(categories)

        category = random.choice(categories)
        tvshow_items = self._apihelper.get_tvshow_items(category['id'])
        self.assertTrue(tvshow_items, msg=category['id'])

        tvshow = random.choice(tvshow_items)
        if tvshow.path.startswith('plugin://plugin.video.vrt.nu/programs/'):
            # When random program has episodes
            episode_items, sort, ascending, content = self._apihelper.get_episode_items(tvshow.path.split('/')[4].replace('.relevant', ''))
            self.assertTrue(episode_items, msg=tvshow.path.split('/')[4])
            self.assertTrue(sort in ['dateadded', 'episode', 'label', 'unsorted'])
            self.assertTrue(ascending is True or ascending is False)
            self.assertTrue(content in ['episodes', 'seasons'], "Content for '%s' is '%s'" % (tvshow.title, content))
        elif tvshow.path.startswith('plugin://plugin.video.vrt.nu/play/id/'):
            # When random program is playable item
            pass
        else:
            self.fail('We did not expect this, either we find episodes or it is a playable item')

    def test_categories(self):
        ''' Test to ensure our hardcoded categories conforms to scraped categories '''
        category_items = self._apihelper.get_category_items()
        self.assertEqual(len(category_items), 17)

    def test_featured(self):
        ''' Test to ensure our hardcoded categories conforms to scraped categories '''
        featured_items = self._apihelper.get_featured_items()
        self.assertEqual(len(featured_items), 7)


if __name__ == '__main__':
    unittest.main()
