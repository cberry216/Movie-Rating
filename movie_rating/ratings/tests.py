from selenium import webdriver
from selenium.webdriver.firefox.options import Options

from django.test import TestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.utils import timezone
from django.core.exceptions import FieldError
from django.shortcuts import reverse

from .helpers import (
    get_item_or_none,
    get_unrated_movies_from_group
)
from .models import Movie, Group, User, Rating

# Create your tests here.


class HelperTestCase(TestCase):
    movie1 = None
    movie2 = None
    movie3 = None
    movie4 = None
    group1 = None
    user1 = None
    user2 = None
    user3 = None
    rating1 = None
    rating2 = None
    rating3 = None
    rating4 = None
    rating5 = None
    rating6 = None
    rating7 = None

    def setUp(self):
        self.movie1 = Movie.objects.create(
            movie_id=1,
            title='First Movie',
            rated='PG',
            released='2006-10-25',
            runtime_minutes=100,
            genre='Horror',
            imdb_rating=6.4,
            rt_rating=67
        )
        self.movie2 = Movie.objects.create(
            movie_id=2,
            title='Second Movie',
            rated='PG-13',
            released='2007-10-25',
            runtime_minutes=120,
            genre='Comedy',
            imdb_rating=2.8,
            rt_rating=54
        )
        self.movie3 = Movie.objects.create(
            movie_id=3,
            title='Third Movie',
            rated='R',
            released='2008-10-25',
            runtime_minutes=90,
            genre='Horror',
            imdb_rating=3.5,
            rt_rating=42,
        )
        self.movie4 = Movie.objects.create(
            movie_id=4,
            title='Fourth Movie',
            rated='G',
            released='2009-10-25',
            runtime_minutes=86,
            genre='Comedy',
            imdb_rating=4.0,
            rt_rating=61,
        )
        self.group1 = Group.objects.create(
            group_id=1,
            group_name='Cool Group'
        )
        self.user1 = User.objects.create(
            user_id=1,
            username='abc',
            first_name='abc',
            email='abc@abc.com',
            group=Group.objects.get(group_id=1)
        )
        self.user2 = User.objects.create(
            user_id=2,
            username='def',
            first_name='def',
            email='def@def.com',
            group=Group.objects.get(group_id=1)
        )
        self.user3 = User.objects.create(
            user_id=3,
            username='hij',
            first_name='hij',
            email='hij@hij.com',
        )
        self.rating1 = Rating.objects.create(
            rating_id=1,
            user=self.user1,
            movie=self.movie1,
            rating=3.7
        )
        self.rating2 = Rating.objects.create(
            rating_id=2,
            user=self.user2,
            movie=self.movie1,
            rating=6.2
        )
        self.rating3 = Rating.objects.create(
            rating_id=3,
            user=self.user3,
            movie=self.movie1,
            rating=8.4
        )
        self.rating4 = Rating.objects.create(
            rating_id=4,
            user=self.user1,
            movie=self.movie2,
            rating=7.8
        )
        self.rating5 = Rating.objects.create(
            rating_id=5,
            user=self.user2,
            movie=self.movie3,
            rating=5.0
        )
        self.rating6 = Rating.objects.create(
            rating_id=6,
            user=self.user1,
            movie=self.movie4,
            rating=6.9
        )
        self.rating7 = Rating.objects.create(
            rating_id=7,
            user=self.user2,
            movie=self.movie4,
            rating=2.0
        )

    def test_get_item_or_none(self):
        passResult1 = Movie.objects.get(movie_id=1)
        testResult1 = get_item_or_none(Movie, movie_id=1)
        testResult2 = get_item_or_none(Movie, movie_id=5)
        self.assertEqual(passResult1, testResult1)
        self.assertEqual(None, testResult2)
        self.assertRaises(FieldError, get_item_or_none, Movie, group_id=1)

    def test_get_unrated_movies_from_group(self):
        list_of_correct_movies1 = [self.movie3]
        qset_of_result_movies1 = get_unrated_movies_from_group(self.user1)
        for movie in qset_of_result_movies1:
            self.assertTrue(movie in list_of_correct_movies1)

        list_of_correct_movies2 = [self.movie2]
        qset_of_result_movies2 = get_unrated_movies_from_group(self.user2)
        for movie in qset_of_result_movies2:
            self.assertTrue(movie in list_of_correct_movies2)

        correct_response3 = None
        test_response3 = get_unrated_movies_from_group(self.user3)
        self.assertEqual(correct_response3, test_response3)


class ViewsTestCase(TestCase):

    movie1 = None
    movie2 = None
    movie3 = None
    movie4 = None
    group1 = None
    user1 = None
    user2 = None
    user3 = None
    rating1 = None
    rating2 = None
    rating3 = None
    rating4 = None
    rating5 = None
    rating6 = None
    rating7 = None

    def setUp(self):
        self.movie1 = Movie.objects.create(
            movie_id=1,
            title='First Movie',
            rated='PG',
            released='2006-10-25',
            runtime_minutes=100,
            genre='Horror',
            imdb_rating=6.4,
            rt_rating=67
        )
        self.movie2 = Movie.objects.create(
            movie_id=2,
            title='Second Movie',
            rated='PG-13',
            released='2007-10-25',
            runtime_minutes=120,
            genre='Comedy',
            imdb_rating=2.8,
            rt_rating=54
        )
        self.movie3 = Movie.objects.create(
            movie_id=3,
            title='Third Movie',
            rated='R',
            released='2008-10-25',
            runtime_minutes=90,
            genre='Horror',
            imdb_rating=3.5,
            rt_rating=42,
        )
        self.movie4 = Movie.objects.create(
            movie_id=4,
            title='Fourth Movie',
            rated='G',
            released='2009-10-25',
            runtime_minutes=86,
            genre='Comedy',
            imdb_rating=4.0,
            rt_rating=61,
        )
        self.group1 = Group.objects.create(
            group_id=1,
            group_name='Cool Group'
        )
        self.user1 = User.objects.create(
            user_id=1,
            username='abc',
            first_name='abc',
            email='abc@abc.com',
            group=Group.objects.get(group_id=1),
        )
        self.user1.set_password('password')
        self.user1.save()
        self.user2 = User.objects.create(
            user_id=2,
            username='def',
            first_name='def',
            email='def@def.com',
            group=Group.objects.get(group_id=1)
        )
        self.user3 = User.objects.create(
            user_id=3,
            username='hij',
            first_name='hij',
            email='hij@hij.com',
        )
        self.rating1 = Rating.objects.create(
            rating_id=1,
            user=self.user1,
            movie=self.movie1,
            rating=3.7
        )
        self.rating2 = Rating.objects.create(
            rating_id=2,
            user=self.user2,
            movie=self.movie1,
            rating=6.2
        )
        self.rating3 = Rating.objects.create(
            rating_id=3,
            user=self.user3,
            movie=self.movie1,
            rating=8.4
        )
        self.rating4 = Rating.objects.create(
            rating_id=4,
            user=self.user1,
            movie=self.movie2,
            rating=7.8
        )
        self.rating5 = Rating.objects.create(
            rating_id=5,
            user=self.user2,
            movie=self.movie3,
            rating=5.0
        )
        self.rating6 = Rating.objects.create(
            rating_id=6,
            user=self.user1,
            movie=self.movie4,
            rating=6.9
        )
        self.rating7 = Rating.objects.create(
            rating_id=7,
            user=self.user2,
            movie=self.movie4,
            rating=2.0
        )

    def test_search_movie_view(self):
        self.client.login(username='abc', password='password')
        self.assertTrue(self.user1.is_authenticated)
        response = self.client.get('/movie/rate-movie/', follow=True)
        self.assertEqual(response.status_code, 200)
        correctUnratedMovies = [self.movie3]
        self.assertEqual(response.context['unrated_group_movies'], correctUnratedMovies)


class HeadlessTestCase(StaticLiveServerTestCase):

    movie1 = None
    movie2 = None
    movie3 = None
    movie4 = None
    group1 = None
    user1 = None
    user2 = None
    user3 = None
    rating1 = None
    rating2 = None
    rating3 = None
    rating4 = None
    rating5 = None
    rating6 = None
    rating7 = None
    driver = None

    def setUp(self):
        super().setUpClass()
        self.movie1 = Movie.objects.create(
            movie_id=1,
            title='First Movie',
            rated='PG',
            released='2006-10-25',
            runtime_minutes=100,
            genre='Horror',
            imdb_rating=6.4,
            rt_rating=67
        )
        self.movie2 = Movie.objects.create(
            movie_id=2,
            title='Second Movie',
            rated='PG-13',
            released='2007-10-25',
            runtime_minutes=120,
            genre='Comedy',
            imdb_rating=2.8,
            rt_rating=54
        )
        self.movie3 = Movie.objects.create(
            movie_id=3,
            title='Third Movie',
            rated='R',
            released='2008-10-25',
            runtime_minutes=90,
            genre='Horror',
            imdb_rating=3.5,
            rt_rating=42,
        )
        self.movie4 = Movie.objects.create(
            movie_id=4,
            title='Fourth Movie',
            rated='G',
            released='2009-10-25',
            runtime_minutes=86,
            genre='Comedy',
            imdb_rating=4.0,
            rt_rating=61,
        )
        self.group1 = Group.objects.create(
            group_id=1,
            group_name='Cool Group'
        )
        self.user1 = User.objects.create(
            user_id=1,
            username='abc',
            first_name='abc',
            email='abc@abc.com',
            group=Group.objects.get(group_id=1),
        )
        self.user1.set_password('password')
        self.user1.save()
        self.user2 = User.objects.create(
            user_id=2,
            username='def',
            first_name='def',
            email='def@def.com',
            group=Group.objects.get(group_id=1)
        )
        self.user3 = User.objects.create(
            user_id=3,
            username='hij',
            first_name='hij',
            email='hij@hij.com',
        )
        self.rating1 = Rating.objects.create(
            rating_id=1,
            user=self.user1,
            movie=self.movie1,
            rating=3.7
        )
        self.rating2 = Rating.objects.create(
            rating_id=2,
            user=self.user2,
            movie=self.movie1,
            rating=6.2
        )
        self.rating3 = Rating.objects.create(
            rating_id=3,
            user=self.user3,
            movie=self.movie1,
            rating=8.4
        )
        self.rating4 = Rating.objects.create(
            rating_id=4,
            user=self.user1,
            movie=self.movie2,
            rating=7.8
        )
        self.rating5 = Rating.objects.create(
            rating_id=5,
            user=self.user2,
            movie=self.movie3,
            rating=5.0
        )
        self.rating6 = Rating.objects.create(
            rating_id=6,
            user=self.user1,
            movie=self.movie4,
            rating=6.9
        )
        self.rating7 = Rating.objects.create(
            rating_id=7,
            user=self.user2,
            movie=self.movie4,
            rating=2.0
        )
        options = Options()
        options.headless = True
        self.driver = webdriver.Firefox(options=options)
        self.driver.implicitly_wait(10)
        self.driver.set_window_size(1366, 768)

    def test_login_headless(self):
        # Login with headless browser
        current_url = f'{self.live_server_url}/login/'
        self.driver.get(f'{self.live_server_url}/login/')
        self.assertEqual(current_url, self.driver.current_url)
        username_input = self.driver.find_element_by_css_selector('input#id_username')
        username_input.clear()
        username_input.send_keys('abc')
        password_input = self.driver.find_element_by_css_selector('input#id_password')
        password_input.clear()
        password_input.send_keys('password')
        login_submit = self.driver.find_element_by_css_selector('input#login_submit')
        login_redirect_url = f'{self.live_server_url}/'
        login_submit.click()
        self.assertEqual(login_redirect_url, self.driver.current_url)

        # Going back to login should redirect to homepage
        self.driver.get(f'{self.live_server_url}/login/')
        self.assertEqual(f'{self.live_server_url}/', self.driver.current_url)

    def test_logout_headless(self):
        # Login with headless browser
        self.driver.get(f'{self.live_server_url}/login/')
        self.assertEqual(f'{self.live_server_url}/login/', self.driver.current_url)
        ui = self.driver.find_element_by_css_selector('input#id_username')
        ui.clear()
        ui.send_keys('abc')
        pi = self.driver.find_element_by_css_selector('input#id_password')
        pi.clear()
        pi.send_keys('password')
        ls = self.driver.find_element_by_css_selector('input#login_submit')
        ls.click()
        self.assertEqual(f'{self.live_server_url}/', self.driver.current_url)

        # Testing logout should return to homepage
        self.driver.get(f'{self.live_server_url}/logout/')
        self.assertEqual(f'{self.live_server_url}/', self.driver.current_url)

        # Going back to login should not redirect to homepage
        self.driver.get(f'{self.live_server_url}/login/')
        self.assertEqual(f'{self.live_server_url}/login/', self.driver.current_url)

        # Going to logout while logged out should redirect to home
        self.driver.get(f'{self.live_server_url}/logout/')
        self.assertEqual(f'{self.live_server_url}/', self.driver.current_url)

    def test_search_movie_headless(self):
        # Going to rate-movie without being logged in should redirect to login
        self.driver.get(f'{self.live_server_url}/movie/rate-movie/')
        self.assertEqual(f'{self.live_server_url}/user/login/?next=/movie/rate-movie/', self.driver.current_url)

        # Login with headless browser
        ui = self.driver.find_element_by_css_selector('input#id_username')
        ui.clear()
        ui.send_keys('abc')
        pi = self.driver.find_element_by_css_selector('input#id_password')
        pi.clear()
        pi.send_keys('password')
        ls = self.driver.find_element_by_css_selector('input#login_submit')
        ls.click()

        # After login, next should redirect to rate-movie
        self.assertEqual(f'{self.live_server_url}/movie/rate-movie/', self.driver.current_url)
        unrated_movies = self.driver.find_elements_by_css_selector('.unrated_movie')
        self.assertEqual(1, len(unrated_movies))
        unrated_movie = unrated_movies[0]
        self.assertEqual(self.movie3, unrated_movie)
