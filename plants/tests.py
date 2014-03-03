"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

"""

from django.test import TestCase


class SimpleTest(TestCase):
    def test_basic_addition(self):
        pass
        self.assertEqual(1 + 1, 2)
