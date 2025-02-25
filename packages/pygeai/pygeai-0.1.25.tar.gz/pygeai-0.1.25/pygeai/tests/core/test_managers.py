from unittest import TestCase
from unittest.mock import MagicMock, patch

from pygeai.core.base.mappers import ResponseMapper
from pygeai.core.base.models import Project
from pygeai.core.base.responses import EmptyResponse
from pygeai.core.managers import Geai
from pygeai.organization.clients import OrganizationClient
from pygeai.organization.mappers import OrganizationResponseMapper
from pygeai.organization.responses import AssistantListResponse, ProjectListResponse, ProjectDataResponse, \
    ProjectTokensResponse, ProjectItemListResponse


class TestGeai(TestCase):
    """
    python -m unittest pygeai.tests.core.test_managers.TestGeai
    """

    def setUp(self):
        self.mock_client = MagicMock(spec=OrganizationClient)
        with patch("pygeai.organization.clients.OrganizationClient", return_value=self.mock_client):
            self.geai = Geai(api_key="test_key", base_url="http://test.url")

    def test_get_assistant_list(self):
        mock_response = AssistantListResponse(assistants=[])

        with patch.object(self.geai._Geai__organization_client, 'get_assistant_list', return_value={}):
            with patch.object(OrganizationResponseMapper, 'map_to_assistant_list_response', return_value=mock_response):
                response = self.geai.get_assistant_list()

        self.assertIsInstance(response, AssistantListResponse)
        self.assertEqual(response.assistants, [])

    def test_get_project_list(self):
        mock_response = ProjectListResponse(projects=[])

        with patch.object(self.geai._Geai__organization_client, 'get_project_list', return_value={}):
            with patch.object(OrganizationResponseMapper, 'map_to_project_list_response', return_value=mock_response):
                response = self.geai.get_project_list()

        self.assertIsInstance(response, ProjectListResponse)
        self.assertEqual(response.projects, [])

    def test_get_project_data(self):
        mock_project = Project(
            id="123",
            name="Test Project",
            description="Test Description",
            email="test@example.com",
            usage_limit=None
        )

        mock_response = ProjectDataResponse(project=mock_project)

        with patch.object(self.geai._Geai__organization_client, 'get_project_data', return_value={}):
            with patch.object(OrganizationResponseMapper, 'map_to_project_data', return_value=mock_response):
                response = self.geai.get_project_data("123")

        self.assertIsInstance(response, ProjectDataResponse)
        self.assertEqual(response.project.name, "Test Project")

    def test_create_project(self):
        mock_project = Project(
            id="123",
            name="New Project",
            description="A test project",
            email="test@example.com",
            usage_limit=None
        )

        mock_response = ProjectDataResponse(project=mock_project)

        with patch.object(self.geai._Geai__organization_client, 'create_project', return_value={}):
            with patch.object(OrganizationResponseMapper, 'map_to_project_data', return_value=mock_response):
                response = self.geai.create_project(mock_project)

        self.assertIsInstance(response, ProjectDataResponse)
        self.assertEqual(response.project.name, "New Project")

    def test_update_project(self):
        mock_project = Project(
            id="123",
            name="Updated Project",
            description="An updated test project",
            email="test@example.com",
            usage_limit=None
        )

        mock_response = ProjectDataResponse(project=mock_project)

        with patch.object(self.geai._Geai__organization_client, 'update_project', return_value={}):
            with patch.object(OrganizationResponseMapper, 'map_to_project_data', return_value=mock_response):
                response = self.geai.update_project(mock_project)

        self.assertIsInstance(response, ProjectDataResponse)
        self.assertEqual(response.project.name, "Updated Project")

    def test_delete_project(self):
        mock_response = EmptyResponse(content={})

        with patch.object(self.geai._Geai__organization_client, 'delete_project', return_value={}):
            with patch.object(ResponseMapper, 'map_to_empty_response', return_value=mock_response):
                response = self.geai.delete_project("123")

        self.assertIsInstance(response, EmptyResponse)
        self.assertEqual(response.content, {})

    def test_get_project_tokens(self):
        mock_response = ProjectTokensResponse(tokens=[])

        with patch.object(self.geai._Geai__organization_client, 'get_project_tokens', return_value={"tokens": []}):
            with patch.object( OrganizationResponseMapper, 'map_to_token_list_response', return_value=mock_response):
                response = self.geai.get_project_tokens("123")

        self.assertIsInstance(response, ProjectTokensResponse)
        self.assertEqual(response.tokens, [])

    def test_export_request_data(self):
        mock_response = MagicMock()
        mock_response.content = '{"items": []}'

        self.mock_client.export_request_data.return_value = mock_response

        with patch.object(self.geai._Geai__organization_client, 'export_request_data', return_value={"items": []}):
            with patch.object(OrganizationResponseMapper, 'map_to_item_list_response', return_value=ProjectItemListResponse(items=[])):
                response = self.geai.export_request_data()

        self.assertIsInstance(response, ProjectItemListResponse)
        self.assertEqual(response.items, [])