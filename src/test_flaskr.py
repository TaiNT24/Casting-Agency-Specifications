import copy
import os
import unittest
import json
from datetime import datetime

from api import create_app
from database.models import setup_db, Actors, Movies, db_drop_and_create_all


class CastingAgencyTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client

        # FOR init local data
        db_drop_and_create_all()

        self.new_actor = {
            "name": "Tai",
            "age": 24,
            "gender": 0
        }

        self.new_movie = {
            "title": "Movie 2",
            "release_date": "2023-03-01"
        }

        # token login with account has role executive producer
        self.token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InpkSENjYWVZeTVpVzZLaTJxNXV1WSJ9.eyJpc3MiOiJodHRwczovL3RhaW50MjQudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDY0MzI1ODliZDhjZDJlODhkMGVhMDZkZCIsImF1ZCI6ImZzbmQiLCJpYXQiOjE2ODEwMzQ4NTYsImV4cCI6MTY4MTEyMTI1NiwiYXpwIjoiTVBsNkM2aXlrOTVNS203TURHNE1WMUNOcmdoVmpCOG4iLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImFkZDphY3RvcnMiLCJhZGQ6bW92aWVzIiwiZGVsZXRlOmFjdG9ycyIsImRlbGV0ZTptb3ZpZXMiLCJyZWFkOmFjdG9ycyIsInJlYWQ6bW92aWVzIiwidXBkYXRlOmFjdG9ycyIsInVwZGF0ZTptb3ZpZXMiXX0.Rdwh3bsxvU__d2T_BgRjurjQ02rTVCQ7PGxvQzZFZ4brTNG4DvexfvlI6udWqHONl_u3Z5v5joDhtJPX_2d57fBvvbjBVwij_7c7UpDBkvrWkFoRXQxE95l3lXvgQRyBTmFgipoDblCtp7B1ECxf43bpE06jpuIIYrS8XjNCadUIkN3HFMBYCaJjBmIkQE4ocND44W03tYo112pl17EsIeIkULmNO46kGMiRh4gsew1XySNnUBeU-bqH8APeFdrLwF03gkyTNzRHBEK8zTAd_ivvYBwNSI6VijC9LBr4-6cIZEiozLomdkbo36utEWaXD9K0kDnjJmGOi8oCeMVYNQ'
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_get_actors(self):
        headers = {'Content-Type': 'application/json', f'Authorization': f'Bearer {self.token}'}

        res = self.client().get('/actors', headers=headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['actors'])

    def test_get_actors_with_no_auth(self):
        res = self.client().get('/actors')
        self.assertEqual(res.status_code, 401)

    def test_get_movies(self):
        headers = {'Content-Type': 'application/json', f'Authorization': f'Bearer {self.token}'}

        res = self.client().get('/movies', headers=headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['movies'])

    def test_get_movies_with_no_auth(self):
        res = self.client().get('/movies')
        self.assertEqual(res.status_code, 401)

    def test_add_actors_fail(self):
        headers = {'Content-Type': 'application/json', f'Authorization': f'Bearer {self.token}'}

        actor = copy.copy(self.new_actor)
        actor.update({'gender': 10})
        res = self.client().post('/actors', headers=headers, json=actor)

        self.assertEqual(res.status_code, 422)

    def test_add_actors_success(self):
        headers = {'Content-Type': 'application/json', f'Authorization': f'Bearer {self.token}'}

        res = self.client().post('/actors', headers=headers, json=self.new_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['actors'])

    def test_delete_actors_success(self):
        headers = {'Content-Type': 'application/json', f'Authorization': f'Bearer {self.token}'}

        res = self.client().delete('/actors/1', headers=headers)

        self.assertEqual(res.status_code, 200)

    def test_delete_actors_404(self):
        headers = {'Content-Type': 'application/json', f'Authorization': f'Bearer {self.token}'}

        res = self.client().delete('/actors/1000', headers=headers)

        self.assertEqual(res.status_code, 404)

    def test_update_actors_success(self):
        headers = {'Content-Type': 'application/json', f'Authorization': f'Bearer {self.token}'}

        res = self.client().patch('/actors/1', headers=headers, json={
            'age':18
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['actor'])

    def test_update_actors_fail(self):
        headers = {'Content-Type': 'application/json', f'Authorization': f'Bearer {self.token}'}

        res = self.client().patch('/actors/1', headers=headers, json={
            'gender': 18
        })

        self.assertEqual(res.status_code, 422)

    def test_update_movies_success(self):
        headers = {'Content-Type': 'application/json', f'Authorization': f'Bearer {self.token}'}

        res = self.client().patch('/movies/1', headers=headers, json={
            'release_date': '2021-10-10'
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['movie'])

    def test_update_movies_fail(self):
        headers = {'Content-Type': 'application/json', f'Authorization': f'Bearer {self.token}'}

        res = self.client().patch('/movies/1', headers=headers, json={
            'release_date': 18
        })

        self.assertEqual(res.status_code, 422)

    def test_add_movies_success(self):
        headers = {'Content-Type': 'application/json', f'Authorization': f'Bearer {self.token}'}

        res = self.client().post('/movies', headers=headers, json=self.new_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['movie'])

    def test_add_movies_fail(self):
        headers = {'Content-Type': 'application/json', f'Authorization': f'Bearer WRONG_TOKEN'}

        res = self.client().post('/movies', headers=headers, json=self.new_movie)

        self.assertEqual(res.status_code, 401)

    def test_delete_movies_success(self):
        headers = {'Content-Type': 'application/json', f'Authorization': f'Bearer {self.token}'}

        res = self.client().delete('/movies/1', headers=headers)

        self.assertEqual(res.status_code, 200)

    def test_delete_movies_404(self):
        headers = {'Content-Type': 'application/json', f'Authorization': f'Bearer {self.token}'}

        res = self.client().delete('/movies/1000', headers=headers)

        self.assertEqual(res.status_code, 404)

    def test_welcome_success(self):
        res = self.client().get('/')

        self.assertEqual(res.status_code, 200)

    def test_logout_success(self):
        res = self.client().get('/logout')

        self.assertEqual(res.status_code, 200)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
