import unittest

import requests_mock

from dbrepo.RestClient import RestClient
from dbrepo.api.dto import Identifier, IdentifierType, SaveIdentifierTitle, Creator, IdentifierTitle, \
    IdentifierDescription, SaveIdentifierDescription, Language, SaveIdentifierFunder, SaveRelatedIdentifier, \
    RelatedIdentifierRelation, RelatedIdentifierType, IdentifierFunder, RelatedIdentifier, UserBrief, \
    IdentifierStatusType, CreateIdentifierCreator
from dbrepo.api.exceptions import MalformedError, ForbiddenError, NotExistsError, AuthenticationError


class IdentifierUnitTest(unittest.TestCase):

    def test_create_identifier_succeeds(self):
        with requests_mock.Mocker() as mock:
            exp = Identifier(id=10,
                             database_id=1,
                             view_id=32,
                             publication_year=2024,
                             publisher='TU Wien',
                             type=IdentifierType.VIEW,
                             language=Language.EN,
                             descriptions=[IdentifierDescription(id=2, description='Test Description')],
                             titles=[IdentifierTitle(id=3, title='Test Title')],
                             funders=[IdentifierFunder(id=4, funder_name='FWF')],
                             related_identifiers=[
                                 RelatedIdentifier(id=7, value='10.12345/abc', relation=RelatedIdentifierRelation.CITES,
                                                   type=RelatedIdentifierType.DOI)],
                             creators=[Creator(id=5, creator_name='Carberry, Josiah')],
                             status=IdentifierStatusType.PUBLISHED,
                             owner=UserBrief(id='8638c043-5145-4be8-a3e4-4b79991b0a16', username='mweise'))
            # mock
            mock.post('/api/identifier', json=exp.model_dump(), status_code=201)
            # test
            client = RestClient(username="a", password="b")
            response = client.create_identifier(
                database_id=1, type=IdentifierType.VIEW,
                titles=[SaveIdentifierTitle(title='Test Title')],
                publisher='TU Wien', publication_year=2024,
                language=Language.EN,
                funders=[SaveIdentifierFunder(funder_name='FWF')],
                related_identifiers=[SaveRelatedIdentifier(value='10.12345/abc',
                                                           relation=RelatedIdentifierRelation.CITES,
                                                           type=RelatedIdentifierType.DOI)],
                descriptions=[SaveIdentifierDescription(description='Test Description')],
                creators=[CreateIdentifierCreator(creator_name='Carberry, Josiah')])
            self.assertEqual(exp, response)

    def test_create_identifier_malformed_fails(self):
        with requests_mock.Mocker() as mock:
            # mock
            mock.post('/api/identifier', status_code=400)
            # test
            try:
                client = RestClient(username="a", password="b")
                response = client.create_identifier(
                    database_id=1, type=IdentifierType.VIEW,
                    titles=[SaveIdentifierTitle(title='Test Title')],
                    descriptions=[SaveIdentifierDescription(description='Test')],
                    publisher='TU Wien', publication_year=2024,
                    creators=[CreateIdentifierCreator(creator_name='Carberry, Josiah')])
            except MalformedError:
                pass

    def test_create_identifier_not_allowed_fails(self):
        with requests_mock.Mocker() as mock:
            # mock
            mock.post('/api/identifier', status_code=403)
            # test
            try:
                client = RestClient(username="a", password="b")
                response = client.create_identifier(
                    database_id=1, type=IdentifierType.VIEW,
                    titles=[SaveIdentifierTitle(title='Test Title')],
                    descriptions=[SaveIdentifierDescription(description='Test')],
                    publisher='TU Wien', publication_year=2024,
                    creators=[CreateIdentifierCreator(creator_name='Carberry, Josiah')])
            except ForbiddenError:
                pass

    def test_create_identifier_not_found_fails(self):
        with requests_mock.Mocker() as mock:
            # mock
            mock.post('/api/identifier', status_code=404)
            # test
            try:
                client = RestClient(username="a", password="b")
                response = client.create_identifier(
                    database_id=1, type=IdentifierType.VIEW,
                    titles=[SaveIdentifierTitle(title='Test Title')],
                    descriptions=[SaveIdentifierDescription(description='Test')],
                    publisher='TU Wien', publication_year=2024,
                    creators=[CreateIdentifierCreator(creator_name='Carberry, Josiah')])
            except NotExistsError:
                pass

    def test_create_identifier_not_auth_fails(self):
        with requests_mock.Mocker() as mock:
            # mock
            mock.post('/api/identifier', status_code=503)
            # test
            try:
                response = RestClient().create_identifier(
                    database_id=1, type=IdentifierType.VIEW,
                    titles=[SaveIdentifierTitle(title='Test Title')],
                    descriptions=[SaveIdentifierDescription(description='Test')],
                    publisher='TU Wien', publication_year=2024,
                    creators=[CreateIdentifierCreator(creator_name='Carberry, Josiah')])
            except AuthenticationError:
                pass

    def test_get_identifiers_succeeds(self):
        with requests_mock.Mocker() as mock:
            exp = [Identifier(id=10,
                              database_id=1,
                              view_id=32,
                              publication_year=2024,
                              publisher='TU Wien',
                              type=IdentifierType.VIEW,
                              language=Language.EN,
                              descriptions=[IdentifierDescription(id=2, description='Test Description')],
                              titles=[IdentifierTitle(id=3, title='Test Title')],
                              funders=[IdentifierFunder(id=4, funder_name='FWF')],
                              related_identifiers=[RelatedIdentifier(id=7, value='10.12345/abc',
                                                                     relation=RelatedIdentifierRelation.CITES,
                                                                     type=RelatedIdentifierType.DOI)],
                              creators=[Creator(id=5, creator_name='Carberry, Josiah')],
                              status=IdentifierStatusType.PUBLISHED,
                              owner=UserBrief(id='8638c043-5145-4be8-a3e4-4b79991b0a16', username='mweise'))]
            # mock
            mock.get('/api/identifiers', json=[exp[0].model_dump()], headers={"Accept": "application/json"})
            # test
            response = RestClient().get_identifiers()
            self.assertEqual(exp, response)


if __name__ == "__main__":
    unittest.main()
