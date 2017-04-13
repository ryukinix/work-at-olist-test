from django.core.management import BaseCommand


# return a tree-like structure representing
# the categories as children and parents
def read_csv(fpath):
    pass


class Command(BaseCommand):
    help = 'Import categories to a channel given a csv file with categories.'

    def add_arguments(self, parser):
        parser.add_argument('channel')
        parser.add_argument('categories')

    def handle(self, *args, **options):
        channel = options['channel']
        csv = options['categories']
        print("Channel: {}".format(channel))
        print("Csv: {}".format(csv))
        print('To be implemented.')
