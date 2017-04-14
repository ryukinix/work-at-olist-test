import os

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

import workatolist
from core.management.commands import importcategories
from core import models

# information about the categories.csv file on root of the project.
# this will be used to test the importcategories and the views
CSV_FPATH = os.path.join(workatolist.settings.BASE_DIR, 'categories.csv')
CSV_MD5HASH = '1a6743d0bc87bfa8df47504754cce6ff'


# Django Management Command importcategories test
class ImportCategoriesCommandTests(TestCase):

    def test_if_csv_file_exists(self):
        self.assertTrue(os.path.exists(CSV_FPATH))

    def test_if_csv_file_match(self):
        import hashlib
        hash_sum = hashlib.md5(open(CSV_FPATH, 'rb').read()).hexdigest()
        self.assertEqual(CSV_MD5HASH, hash_sum)

    def test_insertion_database_on_import_categories(self):
        importcategories.import_categories('channel_test', CSV_FPATH)
        self.assertEqual(23, len(models.Category.objects.all()))

    def test_overwrite_channel_erasing(self):
        importcategories.import_categories('channel_test', CSV_FPATH)
        importcategories.overwrite_channel('channel_test')

        self.assertEqual(0, len(models.Category.objects.all()))
        self.assertEqual('channel_test',
                         models.Channel.objects.get(name='channel_test').name)


class CategoryModelTests(TestCase):

    # records for tests

    def setUp(self):
        self.chan = models.Channel.objects.create(name='CategoryModelTests')
        self.parent = models.Category.objects.create(name='ParentTest',
                                                     channel=self.chan)
        self.cat = models.Category.objects.create(name='CategoryTest',
                                                  channel=self.chan,
                                                  parent=self.parent)
        self.cat_children = models.Category.objects.create(name='ChildrenTest',
                                                           channel=self.chan,
                                                           parent=self.cat)

    def test_creation_of_category(self):
        self.assertEqual(self.cat.name, 'CategoryTest')
        self.assertEqual(self.cat.channel.name, 'CategoryModelTests')

    def test_if_parents_is_correct(self):
        self.assertListEqual(self.parent.parents, [])
        self.assertListEqual(self.cat.parents, [self.parent])
        self.assertListEqual(self.cat_children.parents, [self.parent,
                                                         self.cat])

    def test_if_subcategories_is_correct(self):
        self.chan.save()
        self.parent.save()
        self.cat.save()
        self.cat_children.save()
        self.assertListEqual(self.parent.subcategories, [self.cat])
        self.assertListEqual(self.cat.subcategories, [self.cat_children])
        self.assertListEqual(self.cat_children.subcategories, [])

    def test_if_str_method_is_implemented(self):
        self.assertEqual(self.cat.name, str(self.cat))


class ChannelModelTests(TestCase):

    # records for tests
    def setUp(self):
        self.chan = models.Channel.objects.create(name='ChannelModelTests')
        self.parent = models.Category.objects.create(name='ParentTest',
                                                     channel=self.chan)
        self.cat = models.Category.objects.create(name='CategoryTest',
                                                  channel=self.chan,
                                                  parent=self.parent)
        self.cat_children = models.Category.objects.create(name='ChildrenTest',
                                                           channel=self.chan,
                                                           parent=self.cat)

    def test_creation_of_channel(self):
        self.assertEqual(self.chan.name, 'ChannelModelTests')

    def test_channel_category_set(self):
        self.chan.save()
        self.parent.save()
        self.cat.save()
        self.cat_children.save()
        self.assertListEqual(list(self.chan.category_set.all()),
                             [self.parent, self.cat, self.cat_children])

    def test_delete_on_cascade_categories(self):
        self.chan.delete()
        categories = models.Category.objects.filter(channel=self.chan)
        self.assertEquals(len(categories), 0)

    def test_if_str_method_is_implemented(self):
        self.assertEqual(self.chan.name, str(self.chan))


class ChannelListViewTests(APITestCase):

    def test_channel_list_empty(self):
        url = reverse('core:channel-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_channel_and_list(self):
        url = reverse('core:channel-list')
        chan = models.Channel.objects.create(name='channel-list')
        chan.save()
        response = self.client.get(url, format='json')
        channels = list(map(dict, response.data))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn({'name': chan.name,
                       'identifier': str(chan.identifier)}, channels)


class ChannelDetailViewTests(APITestCase):

    def setUp(self):
        importcategories.import_categories('channel-detail', CSV_FPATH)

    def test_http_404_for_inexistent_channel_lookup(self):
        url = reverse('core:channel-detail',
                      kwargs={'channel_name': 'channel_detail'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_consistency_of_output(self):
        """Test the number o roots categories and total of categories"""
        url = reverse('core:channel-detail',
                      kwargs={'channel_name': 'channel-detail'})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # book, games and computers
        self.assertEqual(len(response.data), 3)
        # all the 23 entries as the number of entries on CSV
        self.assertEqual(self.count_tree(response.data),
                         23)

    def count_tree(self, ordered_dicts):
        """
        Given a tree of categories by subcategories as list of ordered_dicts
        Return the number of nodes on tree (total of categories entries)
        """
        count = 0
        for entry in ordered_dicts:
            if entry['subcategories']:
                elements = 1 + self.count_tree(entry['subcategories'])
            else:
                elements = 1
            count += elements

        return count


class CategoryDetailViewTests(APITestCase):

    def setUp(self):
        importcategories.import_categories('category-detail', CSV_FPATH)

    def test_http_404_for_inexistent_category_lookup(self):
        url = reverse('core:category-detail',
                      kwargs={'channel_name': 'category-detail',
                              'category_name': 'inexistent-category'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_consistency_of_output(self):
        url = reverse('core:category-detail',
                      kwargs={'channel_name': 'category-detail',
                              'category_name': 'computers'})
        response = self.client.get(url, format='json')
        parents = ['books']
        subcategories = ['applications', 'database', 'programming',
                         'notebooks', 'tablets', 'desktop']
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertListEqual(parents,
                             [x['name'] for x in response.data['parents']])
        self.assertListEqual(subcategories,
                             [x['name'] for x in response.data['subcategories']])

