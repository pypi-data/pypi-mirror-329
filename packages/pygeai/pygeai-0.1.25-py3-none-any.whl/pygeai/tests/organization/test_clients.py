import unittest
from unittest import TestCase
from unittest.mock import patch

from pygeai.organization.clients import OrganizationClient
from pygeai.core.base.session import get_session

session = get_session()


class TestOrganizationClient(TestCase):
    """
    python -m unittest pygeai.tests.organization.test_clients.TestOrganizationClient
    """

    @unittest.skipIf(
        not (session.api_key or session.base_url),
        "Skipping test because API_KEY or BASE_URL is not set"
    )
    def test_get_assistant_list_without_mock(self):
        client = OrganizationClient()
        result = client.get_assistant_list()
        self.assertIsNotNone(result)

    @unittest.skipIf(
        not (session.api_key or session.base_url),
        "Skipping test because API_KEY or BASE_URL is not set"
    )
    def test_get_project_list_without_mock(self):
        client = OrganizationClient()
        result = client.get_project_list()
        self.assertIsNotNone(result)

    @unittest.skipIf(
        not (session.api_key or session.base_url),
        "Skipping test because API_KEY or BASE_URL is not set"
    )
    def test_get_request_data_without_mock(self):
        client = OrganizationClient()
        result = client.export_request_data()
        self.assertIsNotNone(result)

    @patch("pygeai.core.services.rest.ApiService.get")
    def test_get_assistant_list(self, mock_get):
        mock_get.return_value.content = '{"assistants": [{"name": "assistant1"}, {"name": "assistant2"}]}'

        client = OrganizationClient()
        result = client.get_assistant_list()

        self.assertIsNotNone(result)
        self.assertEqual(len(result['assistants']), 2)
        self.assertEqual(result['assistants'][0]['name'], "assistant1")
        self.assertEqual(result['assistants'][1]['name'], "assistant2")

    @patch("pygeai.core.services.rest.ApiService.get")
    def test_get_project_list(self, mock_get):
        mock_get.return_value.content = '{"projects": [{"name": "project1"}, {"name": "project2"}]}'

        client = OrganizationClient()
        result = client.get_project_list()

        self.assertIsNotNone(result)
        self.assertEqual(len(result['projects']), 2)
        self.assertEqual(result['projects'][0]['name'], "project1")
        self.assertEqual(result['projects'][1]['name'], "project2")

    @patch("pygeai.core.services.rest.ApiService.get")
    def test_get_project_data(self, mock_get):
        mock_get.return_value.content = '{"project": {"id": "123", "name": "project1"}}'

        client = OrganizationClient()
        result = client.get_project_data("123")

        self.assertIsNotNone(result)
        self.assertEqual(result['project']['name'], "project1")

    @patch("pygeai.core.services.rest.ApiService.post")
    def test_create_project(self, mock_post):
        mock_post.return_value.content = '{"project": {"id": "123", "name": "project1"}}'

        client = OrganizationClient()
        result = client.create_project("project1", "admin@example.com", "A test project")

        self.assertIsNotNone(result)
        self.assertEqual(result['project']['name'], "project1")

    @patch("pygeai.core.services.rest.ApiService.put")
    def test_update_project(self, mock_put):
        mock_put.return_value.content = '{"project": {"id": "123", "name": "updated_project"}}'

        client = OrganizationClient()
        result = client.update_project("123", "updated_project", "Updated description")

        self.assertIsNotNone(result)
        self.assertEqual(result['project']['name'], "updated_project")

    @patch("pygeai.core.services.rest.ApiService.delete")
    def test_delete_project(self, mock_delete):
        mock_delete.return_value.content = '{"status": "deleted"}'

        client = OrganizationClient()
        result = client.delete_project("123")

        self.assertIsNotNone(result)
        self.assertEqual(result['status'], "deleted")

    @patch("pygeai.core.services.rest.ApiService.get")
    def test_get_project_tokens(self, mock_get):
        mock_get.return_value.content = '{"tokens": ["token1", "token2"]}'

        client = OrganizationClient()
        result = client.get_project_tokens("123")

        self.assertIsNotNone(result)
        self.assertEqual(len(result['tokens']), 2)
        self.assertEqual(result['tokens'][0], "token1")
        self.assertEqual(result['tokens'][1], "token2")

    @patch("pygeai.core.services.rest.ApiService.get")
    def test_export_request_data(self, mock_get):
        mock_get.return_value.content = '{"requests": [{"id": "1", "status": "pending"}]}'

        client = OrganizationClient()
        result = client.export_request_data()

        self.assertIsNotNone(result)
        self.assertEqual(len(result['requests']), 1)
        self.assertEqual(result['requests'][0]['status'], "pending")