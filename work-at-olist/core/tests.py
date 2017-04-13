import os

from django.test import TestCase

import workatolist
from core.management.commands import importcategories
from core import models

# This avoid problems on parsing of API response
# and unintentional print on tests runtime
workatolist.settings.DEBUG = False

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


class ChannelListViewTests(TestCase):

    def test_output_of_api(self):
        pass


class ChannelDetailViewTests(TestCase):

    def test_output_of_api(self):
        pass


class CategoryDetailViewTests(TestCase):

    def test_output_of_api(self):
        pass
