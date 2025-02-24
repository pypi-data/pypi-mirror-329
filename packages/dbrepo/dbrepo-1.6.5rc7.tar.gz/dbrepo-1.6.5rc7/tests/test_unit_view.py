import json
import unittest

import requests_mock
from pandas import DataFrame

from dbrepo.RestClient import RestClient
from dbrepo.api.dto import View, ViewColumn, ColumnType, UserBrief
from dbrepo.api.exceptions import ForbiddenError, NotExistsError, MalformedError, AuthenticationError


class ViewUnitTest(unittest.TestCase):

    def test_get_views_empty_succeeds(self):
        with requests_mock.Mocker() as mock:
            # mock
            mock.get('/api/database/1/view', json=[])
            # test
            response = RestClient().get_views(database_id=1)
            self.assertEqual([], response)

    def test_get_views_succeeds(self):
        with requests_mock.Mocker() as mock:
            exp = [View(id=1,
                        name="Data",
                        internal_name="data",
                        database_id=1,
                        initial_view=False,
                        query="SELECT id FROM mytable WHERE deg > 0",
                        query_hash="94c74728b11a690e51d64719868824735f0817b7",
                        owner=UserBrief(id='8638c043-5145-4be8-a3e4-4b79991b0a16', username='mweise'),
                        is_public=True,
                        is_schema_public=True,
                        columns=[ViewColumn(id=1,
                                            ord=0,
                                            name="id",
                                            internal_name="id",
                                            database_id=1,
                                            auto_generated=False,
                                            type=ColumnType.BIGINT,
                                            is_public=True,
                                            is_null_allowed=False)],
                        identifiers=[])]
            # mock
            mock.get('/api/database/1/view', json=[exp[0].model_dump()])
            # test
            response = RestClient().get_views(database_id=1)
            self.assertEqual(exp, response)

    def test_get_views_not_found_fails(self):
        with requests_mock.Mocker() as mock:
            # mock
            mock.get('/api/database/1/view', status_code=404)
            # test
            try:
                response = RestClient().get_views(database_id=1)
            except NotExistsError:
                pass

    def test_get_view_succeeds(self):
        with requests_mock.Mocker() as mock:
            exp = View(id=3,
                       name="Data",
                       internal_name="data",
                       database_id=1,
                       initial_view=False,
                       query="SELECT id FROM mytable WHERE deg > 0",
                       query_hash="94c74728b11a690e51d64719868824735f0817b7",
                       owner=UserBrief(id='8638c043-5145-4be8-a3e4-4b79991b0a16', username='mweise'),
                       is_public=True,
                       is_schema_public=True,
                       columns=[ViewColumn(id=1,
                                           ord=0,
                                           name="id",
                                           internal_name="id",
                                           database_id=1,
                                           auto_generated=False,
                                           type=ColumnType.BIGINT,
                                           is_public=True,
                                           is_null_allowed=False)],
                       identifiers=[])
            # mock
            mock.get('/api/database/1/view/3', json=exp.model_dump())
            # test
            response = RestClient().get_view(database_id=1, view_id=3)
            self.assertEqual(exp, response)

    def test_get_view_not_allowed_fails(self):
        with requests_mock.Mocker() as mock:
            # mock
            mock.get('/api/database/1/view/3', status_code=403)
            # test
            try:
                response = RestClient().get_view(database_id=1, view_id=3)
            except ForbiddenError:
                pass

    def test_get_views_not_found_fails(self):
        with requests_mock.Mocker() as mock:
            # mock
            mock.get('/api/database/1/view/3', status_code=404)
            # test
            try:
                response = RestClient().get_view(database_id=1, view_id=3)
            except NotExistsError:
                pass

    def test_create_view_succeeds(self):
        with requests_mock.Mocker() as mock:
            exp = View(id=3,
                       name="Data",
                       internal_name="data",
                       database_id=1,
                       initial_view=False,
                       query="SELECT id FROM mytable WHERE deg > 0",
                       query_hash="94c74728b11a690e51d64719868824735f0817b7",
                       owner=UserBrief(id='8638c043-5145-4be8-a3e4-4b79991b0a16', username='mweise'),
                       is_public=True,
                       is_schema_public=True,
                       columns=[ViewColumn(id=1,
                                           ord=0,
                                           name="id",
                                           internal_name="id",
                                           database_id=1,
                                           auto_generated=False,
                                           type=ColumnType.BIGINT,
                                           is_public=True,
                                           is_null_allowed=False)],
                       identifiers=[])
            # mock
            mock.post('/api/database/1/view', json=exp.model_dump(), status_code=201)
            # test
            client = RestClient(username="a", password="b")
            response = client.create_view(database_id=1, name="Data", is_public=True, is_schema_public=True,
                                          query="SELECT id FROM mytable WHERE deg > 0")
            self.assertEqual(exp, response)

    def test_create_view_malformed_fails(self):
        with requests_mock.Mocker() as mock:
            # mock
            mock.post('/api/database/1/view', status_code=400)
            # test
            try:
                client = RestClient(username="a", password="b")
                response = client.create_view(database_id=1, name="Data", is_public=True, is_schema_public=True,
                                              query="SELECT id FROM mytable WHERE deg > 0")
            except MalformedError:
                pass

    def test_create_view_not_allowed_fails(self):
        with requests_mock.Mocker() as mock:
            # mock
            mock.post('/api/database/1/view', status_code=403)
            # test
            try:
                client = RestClient(username="a", password="b")
                response = client.create_view(database_id=1, name="Data", is_public=True, is_schema_public=True,
                                              query="SELECT id FROM mytable WHERE deg > 0")
            except ForbiddenError:
                pass

    def test_create_view_not_found_fails(self):
        with requests_mock.Mocker() as mock:
            # mock
            mock.post('/api/database/1/view', status_code=404)
            # test
            try:
                client = RestClient(username="a", password="b")
                response = client.create_view(database_id=1, name="Data", is_public=True, is_schema_public=True,
                                              query="SELECT id FROM mytable WHERE deg > 0")
            except NotExistsError:
                pass

    def test_create_view_not_auth_fails(self):
        with requests_mock.Mocker() as mock:
            # mock
            mock.post('/api/database/1/view', status_code=404)
            # test
            try:
                response = RestClient().create_view(database_id=1, name="Data", is_public=True, is_schema_public=True,
                                                    query="SELECT id FROM mytable WHERE deg > 0")
            except AuthenticationError:
                pass

    def test_delete_view_succeeds(self):
        with requests_mock.Mocker() as mock:
            # mock
            mock.delete('/api/database/1/view/3', status_code=202)
            # test
            client = RestClient(username="a", password="b")
            client.delete_view(database_id=1, view_id=3)

    def test_delete_view_malformed_fails(self):
        with requests_mock.Mocker() as mock:
            # mock
            mock.delete('/api/database/1/view/3', status_code=400)
            # test
            try:
                client = RestClient(username="a", password="b")
                client.delete_view(database_id=1, view_id=3)
            except MalformedError:
                pass

    def test_delete_view_not_allowed_fails(self):
        with requests_mock.Mocker() as mock:
            # mock
            mock.delete('/api/database/1/view/3', status_code=403)
            # test
            try:
                client = RestClient(username="a", password="b")
                client.delete_view(database_id=1, view_id=3)
            except ForbiddenError:
                pass

    def test_delete_view_not_auth_fails(self):
        with requests_mock.Mocker() as mock:
            # mock
            mock.delete('/api/database/1/view/3', status_code=403)
            # test
            try:
                RestClient().delete_view(database_id=1, view_id=3)
            except AuthenticationError:
                pass

    def test_get_view_data_succeeds(self):
        with requests_mock.Mocker() as mock:
            exp = [{'id': 1, 'username': 'foo'}, {'id': 2, 'username': 'bar'}]
            df = DataFrame.from_records(json.dumps(exp))
            # mock
            mock.get('/api/database/1/view/3/data', json=json.dumps(exp))
            # test
            response = RestClient().get_view_data(database_id=1, view_id=3)
            self.assertTrue(DataFrame.equals(df, response))

    def test_get_view_data_dataframe_succeeds(self):
        with requests_mock.Mocker() as mock:
            exp = [{'id': 1, 'username': 'foo'}, {'id': 2, 'username': 'bar'}]
            df = DataFrame.from_records(json.dumps(exp))
            # mock
            mock.get('/api/database/1/view/3/data', json=json.dumps(exp))
            # test
            response: DataFrame = RestClient().get_view_data(database_id=1, view_id=3)
            self.assertEqual(df.shape, response.shape)
            self.assertTrue(DataFrame.equals(df, response))

    def test_get_view_data_malformed_fails(self):
        with requests_mock.Mocker() as mock:
            # mock
            mock.get('/api/database/1/view/3/data', status_code=400)
            # test
            try:
                response = RestClient().get_view_data(database_id=1, view_id=3)
            except MalformedError:
                pass

    def test_get_view_data_not_allowed_fails(self):
        with requests_mock.Mocker() as mock:
            # mock
            mock.get('/api/database/1/view/3/data', status_code=403)
            # test
            try:
                response = RestClient().get_view_data(database_id=1, view_id=3)
            except ForbiddenError:
                pass

    def test_get_view_data_count_succeeds(self):
        with requests_mock.Mocker() as mock:
            exp = 844737
            # mock
            mock.head('/api/database/1/view/3/data', headers={'X-Count': str(exp)})
            # test
            response = RestClient().get_view_data_count(database_id=1, view_id=3)
            self.assertEqual(exp, response)

    def test_get_view_data_count_malformed_fails(self):
        with requests_mock.Mocker() as mock:
            # mock
            mock.head('/api/database/1/view/3/data', status_code=400)
            # test
            try:
                response = RestClient().get_view_data_count(database_id=1, view_id=3)
            except MalformedError:
                pass

    def test_get_view_data_count_not_allowed_fails(self):
        with requests_mock.Mocker() as mock:
            # mock
            mock.head('/api/database/1/view/3/data', status_code=403)
            # test
            try:
                response = RestClient().get_view_data_count(database_id=1, view_id=3)
            except ForbiddenError:
                pass


if __name__ == "__main__":
    unittest.main()
