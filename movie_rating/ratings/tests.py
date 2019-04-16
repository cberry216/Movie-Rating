from django.test import TestCase
from django.utils import timezone
from django.core.exceptions import FieldError

from .helpers import get_item_or_none
from .models import Movie

# Create your tests here.


class HelperTestCase(TestCase):
    def setUp(self):
        Movie.objects.create(
            movie_id=1,
            title='First Movie',
            rated='PG',
            released='2006-10-25',
            runtime_minutes=100
        )

    def test_get_item_or_none(self):
        passResult1 = Movie.objects.get(movie_id=1)
        testResult1 = get_item_or_none(Movie, movie_id=1)
        testResult2 = get_item_or_none(Movie, movie_id=2)
        self.assertEqual(passResult1, testResult1)
        self.assertEqual(None, testResult2)
        self.assertRaises(FieldError, get_item_or_none, Movie, group_id=1)
