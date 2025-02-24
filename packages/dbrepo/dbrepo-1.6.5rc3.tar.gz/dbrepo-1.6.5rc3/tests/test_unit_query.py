import json
import unittest

import requests_mock
import datetime

from dbrepo.RestClient import RestClient
from pandas import DataFrame

from dbrepo.api.dto import Query, User, UserAttributes, QueryType, UserBrief
from dbrepo.api.exceptions import MalformedError, NotExistsError, ForbiddenError


class QueryUnitTest(unittest.TestCase):

    def test_create_subset_succeeds(self):
        with requests_mock.Mocker() as mock:
            exp = [{'id': 1, 'username': 'foo'}, {'id': 2, 'username': 'bar'}]
            df = DataFrame.from_records(json.dumps(exp))
            # mock
            mock.post('/api/database/1/subset', json=json.dumps(exp), headers={'X-Id': '1'}, status_code=201)
            # test
            client = RestClient(username="a", password="b")
            response = client.create_subset(database_id=1, page=0, size=10,
                                            query="SELECT id, username FROM some_table WHERE id IN (1,2)")
            self.assertTrue(DataFrame.equals(df, response))

    def test_create_subset_malformed_fails(self):
        with requests_mock.Mocker() as mock:
            # mock
            mock.post('/api/database/1/subset', status_code=400)
            # test
            try:
                client = RestClient(username="a", password="b")
                response = client.create_subset(database_id=1,
                                                query="SELECT id, username FROM some_table WHERE id IN (1,2)")
            except MalformedError:
                pass

    def test_create_subset_not_allowed_fails(self):
        with requests_mock.Mocker() as mock:
            # mock
            mock.post('/api/database/1/subset', status_code=403)
            # test
            try:
                client = RestClient(username="a", password="b")
                response = client.create_subset(database_id=1,
                                                query="SELECT id, username FROM some_table WHERE id IN (1,2)")
            except ForbiddenError:
                pass

    def test_create_subset_not_found_fails(self):
        with requests_mock.Mocker() as mock:
            # mock
            mock.post('/api/database/1/subset', status_code=404)
            # test
            try:
                client = RestClient(username="a", password="b")
                response = client.create_subset(database_id=1,
                                                query="SELECT id, username FROM some_table WHERE id IN (1,2)")
            except NotExistsError:
                pass

    def test_create_subset_not_auth_succeeds(self):
        with requests_mock.Mocker() as mock:
            exp = [{'id': 1, 'username': 'foo'}, {'id': 2, 'username': 'bar'}]
            df = DataFrame.from_records(json.dumps(exp))
            # mock
            mock.post('/api/database/1/subset', json=json.dumps(exp), headers={'X-Id': '1'}, status_code=201)
            # test

            client = RestClient()
            response = client.create_subset(database_id=1, page=0, size=10,
                                            query="SELECT id, username FROM some_table WHERE id IN (1,2)")
            self.assertTrue(DataFrame.equals(df, response))

    def test_find_query_succeeds(self):
        with requests_mock.Mocker() as mock:
            exp = Query(id=6,
                        owner=UserBrief(id='8638c043-5145-4be8-a3e4-4b79991b0a16', username='mweise'),
                        execution=datetime.datetime(2024, 1, 1, 0, 0, 0, 0, datetime.timezone.utc),
                        query='SELECT id, username FROM some_table WHERE id IN (1,2)',
                        query_normalized='SELECT id, username FROM some_table WHERE id IN (1,2)',
                        type=QueryType.QUERY,
                        database_id=1,
                        query_hash='da5ff66c4a57683171e2ffcec25298ee684680d1e03633cd286f9067d6924ad8',
                        result_hash='464740ba612225913bb15b26f13377707949b55e65288e89c3f8b4c6469aecb4',
                        is_persisted=False,
                        result_number=None,
                        identifiers=[])
            # mock
            mock.get('/api/database/1/subset/6', json=exp.model_dump())
            # test
            response = RestClient().get_subset(database_id=1, subset_id=6)
            self.assertEqual(exp, response)

    def test_find_query_not_allowed_fails(self):
        with requests_mock.Mocker() as mock:
            # mock
            mock.get('/api/database/1/subset/6', status_code=403)
            # test
            try:
                response = RestClient().get_subset(database_id=1, subset_id=6)
            except ForbiddenError:
                pass

    def test_find_query_not_found_fails(self):
        with requests_mock.Mocker() as mock:
            # mock
            mock.get('/api/database/1/subset/6', status_code=404)
            # test
            try:
                response = RestClient().get_subset(database_id=1, subset_id=6)
            except NotExistsError:
                pass

    def test_get_queries_empty_succeeds(self):
        with requests_mock.Mocker() as mock:
            exp = []
            # mock
            mock.get('/api/database/1/subset', json=[])
            # test
            response = RestClient().get_queries(database_id=1)
            self.assertEqual(exp, response)

    def test_get_queries_succeeds(self):
        with requests_mock.Mocker() as mock:
            exp = [Query(id=6,
                         owner=UserBrief(id='8638c043-5145-4be8-a3e4-4b79991b0a16', username='mweise'),
                         execution=datetime.datetime(2024, 1, 1, 0, 0, 0, 0, datetime.timezone.utc),
                         query='SELECT id, username FROM some_table WHERE id IN (1,2)',
                         query_normalized='SELECT id, username FROM some_table WHERE id IN (1,2)',
                         type=QueryType.QUERY,
                         database_id=1,
                         query_hash='da5ff66c4a57683171e2ffcec25298ee684680d1e03633cd286f9067d6924ad8',
                         result_hash='464740ba612225913bb15b26f13377707949b55e65288e89c3f8b4c6469aecb4',
                         is_persisted=False,
                         result_number=None,
                         identifiers=[])]
            # mock
            mock.get('/api/database/1/subset', json=[exp[0].model_dump()])
            # test
            response = RestClient().get_queries(database_id=1)
            self.assertEqual(exp, response)

    def test_get_queries_not_allowed_fails(self):
        with requests_mock.Mocker() as mock:
            # mock
            mock.get('/api/database/1/subset', status_code=403)
            # test
            try:
                response = RestClient().get_queries(database_id=1)
            except ForbiddenError:
                pass

    def test_get_queries_not_found_fails(self):
        with requests_mock.Mocker() as mock:
            # mock
            mock.get('/api/database/1/subset', status_code=404)
            # test
            try:
                response = RestClient().get_queries(database_id=1)
            except NotExistsError:
                pass

    def test_get_subset_data_succeeds(self):
        with requests_mock.Mocker() as mock:
            exp = [{'id': 1, 'username': 'foo'}, {'id': 2, 'username': 'bar'}]
            df = DataFrame.from_records(json.dumps(exp))
            # mock
            mock.get('/api/database/1/subset/6/data', json=json.dumps(exp))
            # test
            response = RestClient().get_subset_data(database_id=1, subset_id=6)
            self.assertTrue(DataFrame.equals(df, response))

    def test_get_subset_data_dataframe_succeeds(self):
        with requests_mock.Mocker() as mock:
            exp = [{'id': 1, 'username': 'foo'}, {'id': 2, 'username': 'bar'}]
            df = DataFrame.from_records(json.dumps(exp))
            # mock
            mock.get('/api/database/1/subset/6/data', json=json.dumps(exp))
            # test
            response = RestClient().get_subset_data(database_id=1, subset_id=6)
            self.assertEqual(df.shape, response.shape)
            self.assertTrue(DataFrame.equals(df, response))

    def test_get_subset_data_not_allowed_fails(self):
        with requests_mock.Mocker() as mock:
            # mock
            mock.get('/api/database/1/subset/6/data', status_code=403)
            # test
            try:
                response = RestClient().get_subset_data(database_id=1, subset_id=6)
            except ForbiddenError:
                pass

    def test_get_subset_data_not_found_fails(self):
        with requests_mock.Mocker() as mock:
            # mock
            mock.get('/api/database/1/subset/6/data', status_code=404)
            # test
            try:
                response = RestClient().get_subset_data(database_id=1, subset_id=6)
            except NotExistsError:
                pass

    def test_get_subset_data_count_succeeds(self):
        with requests_mock.Mocker() as mock:
            exp = 2
            # mock
            mock.head('/api/database/1/subset/6/data', headers={'X-Count': str(exp)})
            # test
            response = RestClient().get_subset_data_count(database_id=1, subset_id=6)
            self.assertEqual(exp, response)

    def test_get_subset_data_count_not_allowed_fails(self):
        with requests_mock.Mocker() as mock:
            # mock
            mock.head('/api/database/1/subset/6/data', status_code=403)
            # test
            try:
                response = RestClient().get_subset_data_count(database_id=1, subset_id=6)
            except ForbiddenError:
                pass

    def test_get_subset_data_count_not_found_fails(self):
        with requests_mock.Mocker() as mock:
            # mock
            mock.head('/api/database/1/subset/6/data', status_code=404)
            # test
            try:
                response = RestClient().get_subset_data_count(database_id=1, subset_id=6)
            except NotExistsError:
                pass


if __name__ == "__main__":
    unittest.main()
