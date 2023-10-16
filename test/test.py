from unittest import TestCase, main, mock
from unittest.mock import Mock, patch
import collections
collections.Callable = collections.abc.Callable
from nose.tools import assert_is_not_none

from app import getTopMovies, getTopTrendingMovies;

class GetTopMoviesTest(TestCase):
    def test_getting_top_movies(self):
        with patch('app.requests.get') as mock_get:
            #Arrange
            mock_get.return_value.ok = True
            #Act
            response = getTopMovies()
            #Assert
            assert_is_not_none(response)

    def test_getting_top_trending_movies(self):
        with patch('app.requests.get') as mock_get:
            #Arrange
            mock_get.return_value.ok = True
            #Act
            response = getTopTrendingMovies()
            #Assert
            assert_is_not_none(response)


if __name__ == "__main__":
    main()
