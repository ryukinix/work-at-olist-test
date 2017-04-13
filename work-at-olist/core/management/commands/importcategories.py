import csv

from django.core.management import BaseCommand

from core.models import Category, Channel


def read_csv(fpath):
    """Return a generator of lines from a csv file"""
    with open(fpath) as csv_file:
        csv_content = csv.reader(csv_file, delimiter=',')
        next(csv_content)  # drop header
        for line in csv_content:
            yield line[0]  # use generator to be memory-friendly


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


def get_last_parent(categories, channel):
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


class Command(BaseCommand):

    help = 'Import categories to a channel given a csv file with categories.'

    def add_arguments(self, parser):
        """Add the channel & categories as arguments"""
        parser.add_argument('channel_name')
        parser.add_argument('csv_categories')

    def handle(self, *args, **options):
        channel_name = options['channel_name']
        channel = overwrite_channel(channel_name)
        csv_path = options['csv_categories']
        for category_path in read_csv(csv_path):
            parent = None
            categories = [x.strip().lower() for x in category_path.split('/')]
            parent = get_last_parent(categories, channel)
            name = categories[-1]
            (cat, created) = Category.objects.get_or_create(name=name,
                                                            parent=parent,
                                                            channel=channel)
            if created:
                cat.save()
