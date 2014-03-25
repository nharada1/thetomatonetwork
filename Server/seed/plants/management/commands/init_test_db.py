from django.core.management.base import BaseCommand, CommandError
from plants.models import Plant
from algo.tests import initTestDB


class Command(BaseCommand):
    help = 'Initializes test database of plots'

    def handle(self, *args, **options):
        initTestDB()

