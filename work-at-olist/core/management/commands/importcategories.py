import csv

from django.core.management import BaseCommand
from django.db import transaction

from core.models import Category, Channel
from workatolist import settings

# help functions are prefixed with _


def _read_csv(fpath):
    """Return a generator of lines from a csv file"""
    with open(fpath) as csv_file:
        csv_content = csv.reader(csv_file, delimiter=',')
        next(csv_content)  # drop header
        for line in csv_content:
            yield line[0]  # use generator to be memory-friendly


def _get_last_parent(categories, channel):
    """
    Fetch iteratively the category path list until
    get the last parent
    """
    if len(categories) == 1:
        return None

    parent = None
    for name in categories[:-1]:
        parent = Category.objects.get(name=name,
                                      parent=parent,
                                      channel=channel)
    return parent


def overwrite_channel(channel_name):
    """
    Create a new channel, save and return it
    if already exists, before return drop all its categories related
    """
    # try delete before
    try:
        Channel.objects.get(name=channel_name).delete()
    except:
        pass
    finally:  # create a new channel anyways
        channel = Channel.objects.create(name=channel_name)
        channel.save()
        return channel


# speed-up insert from hell (incredible improvement)
@transaction.atomic
def import_categories(channel_name, csv_path):
    """
    Insert all categories on database with a new channel instance
    Full update mode: all the earlier categories will be overwritten.
    """
    channel = overwrite_channel(channel_name)
    for category_path in _read_csv(csv_path):
        parent = None
        categories = [x.strip().lower().replace(' ', '-')
                      for x in category_path.split('/')]
        parent = _get_last_parent(categories, channel)
        name = categories[-1]
        (cat, created) = Category.objects.get_or_create(name=name,
                                                        parent=parent,
                                                        channel=channel)
        if created:
            cat.save()
            if settings.DEBUG:
                print('Category created: {} - {}'.format(parent, name))


class Command(BaseCommand):

    help = 'Import categories to a channel given a csv file with categories.'

    def add_arguments(self, parser):
        """Add the channel & categories as arguments"""
        parser.add_argument('channel_name')
        parser.add_argument('csv_categories')

    def handle(self, *args, **options):
        channel_name = options['channel_name'].lower()
        csv_path = options['csv_categories']
        import_categories(channel_name, csv_path)
