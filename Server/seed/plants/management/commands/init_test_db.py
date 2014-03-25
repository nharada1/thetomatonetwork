from django.core.management.base import BaseCommand
from algo.tests import initTestDB


class Command(BaseCommand):
    help = 'Initializes test database of plots'

    def handle(self, *args, **options):
        initTestDB()

