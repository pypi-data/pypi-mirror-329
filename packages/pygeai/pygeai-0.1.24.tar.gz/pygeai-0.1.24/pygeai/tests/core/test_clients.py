import unittest
from unittest import TestCase
from unittest.mock import patch

from pygeai.core.base.models import Project, TextAssistant, LlmSettings, WelcomeData, ChatAssistant, Assistant
from pygeai.core.base.responses import EmptyResponse, ErrorListResponse
from pygeai.core.managers import Geai
from pygeai.organization.responses import AssistantListResponse, ProjectListResponse, ProjectDataResponse, \
    ProjectTokensResponse, ProjectItemListResponse


class TestGeai(TestCase):
    """
    python -m unittest pygeai.tests.core.test_clients.TestGeai
    """

    def setUp(self):
        self.client = Geai()

    @unittest.skip("Requires call to API")
    def test_get_assistant_list(self):
        result = self.client.get_assistant_list()

        self.assertIsNotNone(result)
        self.assertTrue(isinstance(result, AssistantListResponse))

    @unittest.skip("Requires call to API")
    def test_get_project_list(self):
        result = self.client.get_project_list()

        self.assertIsNotNone(result)
        self.assertTrue(isinstance(result, ProjectListResponse))

    @unittest.skip("Requires call to API")
    def test_get_project_data(self):
        result = self.client.get_project_data("2ca6883f-6778-40bb-bcc1-85451fb11107")

        self.assertIsNotNone(result)
        self.assertTrue(isinstance(result, ProjectDataResponse))

    @unittest.skip("Requires call to API")
    def test_create_project_simple(self):
        project = Project(
            project_name="Test project - SDK",
            project_email="alejandro.trinidad@globant.com",
            project_description="Test project to validate programmatic creation of project"
        )
        response = self.client.create_project(project)
        self.assertIsNotNone(response)

    @patch("pygeai.organization.clients.OrganizationClient.get_assistant_list")
    def test_get_assistant_list_mocked(self, mock_get_assistant_list):
        """Test get_assistant_list with a mocked API response."""
        mock_get_assistant_list.return_value = {
            "assistants": [
                {
                    "assistantName": "Test assistant 1",
                },
                {
                    "assistantName": "Test assistant 2",
                },
            ],
            'projectId': 'proj-123',
            'projectName': "Test Project"
        }
        result = self.client.get_assistant_list()
        self.assertIsInstance(result, AssistantListResponse)

    @patch("pygeai.organization.clients.OrganizationClient.get_project_list")
    def test_get_project_list_mocked(self, mock_get_project_list):
        """Test get_project_list with a mocked API response."""
        mock_get_project_list.return_value = {"projects": []}
        result = self.client.get_project_list()
        self.assertIsInstance(result, ProjectListResponse)

    @patch("pygeai.organization.clients.OrganizationClient.get_project_data")
    def test_get_project_data_mocked(self, mock_get_project_data):
        """Test get_project_data with a mocked API response."""
        mock_get_project_data.return_value = {"projectId": "123", "projectName": "Test Project"}
        result = self.client.get_project_data("123")
        self.assertIsInstance(result, ProjectDataResponse)

    @patch("pygeai.organization.clients.OrganizationClient.create_project")
    def test_create_project_mocked(self, mock_create_project):
        """Test create_project with a mocked API response."""
        mock_create_project.return_value = {"projectId": "123", "projectName": "Test Project"}
        project = Project(name="Test Project", email="test@example.com", description="Description")
        response = self.client.create_project(project)
        self.assertIsInstance(response, ProjectDataResponse)

    @patch("pygeai.organization.clients.OrganizationClient.update_project")
    def test_update_project_mocked(self, mock_update_project):
        """Test update_project with a mocked API response."""
        mock_update_project.return_value = {"projectId": "123", "projectName": "Updated Project"}
        project = Project(name="Updated Project", email="test@example.com", description="Updated description")
        response = self.client.update_project(project)
        self.assertIsInstance(response, ProjectDataResponse)

    @patch("pygeai.organization.clients.OrganizationClient.delete_project")
    def test_delete_project_mocked(self, mock_delete_project):
        """Test delete_project with a mocked API response."""
        mock_delete_project.return_value = {}
        response = self.client.delete_project("123")
        self.assertIsInstance(response, EmptyResponse)

    @patch("pygeai.organization.clients.OrganizationClient.get_project_tokens")
    def test_get_project_tokens_mocked(self, mock_get_project_tokens):
        """Test get_project_tokens with a mocked API response."""
        mock_get_project_tokens.return_value = {"tokens": []}
        result = self.client.get_project_tokens("123")
        self.assertIsInstance(result, ProjectTokensResponse)

    @patch("pygeai.organization.clients.OrganizationClient.export_request_data")
    def test_export_request_data_mocked(self, mock_export_request_data):
        """Test export_request_data with a mocked API response."""
        mock_export_request_data.return_value = {"items": []}
        result = self.client.export_request_data()
        self.assertIsInstance(result, ProjectItemListResponse)

    @patch("pygeai.assistant.clients.AssistantClient.get_assistant_data")
    def test_get_assistant_data_mocked(self, mock_get_assistant_data):
        """Test get_assistant_data with a mocked API response."""
        mock_get_assistant_data.return_value = {
            "assistantId": "123",
            "assistantName": "Test Assistant"
        }
        result = self.client.get_assistant_data(assistant_id="123")
        self.assertIsInstance(result, Assistant)

    @patch("pygeai.organization.clients.OrganizationClient.get_project_data")
    def test_get_project_data_error_handling(self, mock_get_project_data):
        mock_get_project_data.return_value = {"errors": [{"id": 404, "description": "Project not found"}]}
        response = self.client.get_project_data("invalid_id")
        self.assertTrue(isinstance(response, ErrorListResponse))
        self.assertTrue(hasattr(response, "errors"))
        error = response.errors[0]
        self.assertEqual(error.id, 404)
        self.assertEqual(error.description, "Project not found")
        self.assertEqual(str(error), "{'id': 404, 'description': 'Project not found'}")

    @patch("pygeai.organization.clients.OrganizationClient.delete_project")
    def test_delete_project_error_handling(self, mock_delete_project):
        mock_delete_project.return_value = {"errors": [{"id": 403, "description": "Permission denied"}]}
        response = self.client.delete_project("invalid_id")
        self.assertTrue(isinstance(response, ErrorListResponse))
        self.assertTrue(hasattr(response, "errors"))
        error = response.errors[0]
        self.assertEqual(error.id, 403)
        self.assertEqual(error.description, "Permission denied")
        self.assertEqual(str(error), "{'id': 403, 'description': 'Permission denied'}")

    @patch("pygeai.assistant.clients.AssistantClient.create_assistant")
    def test_create_text_assistant_mocked(self, mock_create_assistant):
        """Test create_text_assistant with a mocked API response."""
        mock_create_assistant.return_value = {"projectId": "123", "projectName": "Test Project"}

        llm_settings = LlmSettings(provider_name="openai", model_name="GPT-4", temperature=0.7)
        welcome_data = WelcomeData(title="Welcome!", description="Welcome to the assistant")
        assistant = TextAssistant(
            name="Text Assistant",
            prompt="Prompt",
            description="Description",
            llm_settings=llm_settings,
            welcome_data=welcome_data
        )

        response = self.client.create_text_assistant(assistant)
        self.assertIsInstance(response, Project)

    @patch("pygeai.assistant.clients.AssistantClient.create_assistant")
    def test_create_chat_assistant_mocked(self, mock_create_assistant):
        """Test create_chat_assistant with a mocked API response."""
        mock_create_assistant.return_value = {"projectId": "456", "projectName": "Test Project"}

        llm_settings = LlmSettings(provider_name="openai", model_name="GPT-4", temperature=0.8)
        welcome_data = WelcomeData(title="Hello!", description="Welcome to the assistant")
        assistant = ChatAssistant(
            name="Chat Assistant",
            prompt="Chat Prompt",
            description="Description",
            llm_settings=llm_settings,
            welcome_data=welcome_data
        )

        response = self.client.create_chat_assistant(assistant)
        self.assertIsInstance(response, Project)
