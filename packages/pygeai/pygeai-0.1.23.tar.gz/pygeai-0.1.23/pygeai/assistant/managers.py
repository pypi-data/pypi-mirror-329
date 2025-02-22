from typing import Any

from pygeai.assistant.clients import AssistantClient
from pygeai.assistant.rag.clients import RAGAssistantClient
from pygeai.assistant.rag.mappers import RAGAssistantMapper
from pygeai.assistant.rag.responses import DocumentListResponse
from pygeai.core.base.mappers import ErrorMapper, ResponseMapper
from pygeai.core.base.models import Assistant, TextAssistant, ChatAssistant, ChatMessageList, AssistantRevision, \
    ChatVariableList, LlmSettings
from pygeai.core.base.responses import EmptyResponse
from pygeai.core.mappers import AssistantResponseMapper
from pygeai.core.responses import NewAssistantResponse, ChatResponse
from pygeai.chat.clients import ChatClient
from pygeai.assistant.rag.models import RAGAssistant, Document, UploadDocument
from pygeai.core.common.exceptions import MissingRequirementException


class AssistantManager:

    def __init__(self, api_key: str = None, base_url: str = None, alias: str = "default"):
        self.__assistant_client = AssistantClient(api_key, base_url, alias)
        self.__chat_client = ChatClient(api_key, base_url, alias)
        self.__rag_client = RAGAssistantClient(api_key, base_url, alias)

    def get_assistant_data(
            self,
            assistant_id: str = None,
            detail: str = "summary",
            assistant_name: str = None
    ) -> Assistant:
        """
        Retrieves assistant data using either an assistant ID or an assistant name. RAG Assistants are searched by name
        and Text or Chat Assistants are searched by ID.

        This method fetches assistant details by calling either `_get_assistant_data_by_id`
        or `_get_assistant_data_by_name`, depending on the provided parameters.

        - If `assistant_id` is provided, it retrieves the assistant using `_get_assistant_data_by_id`.
        - If `assistant_name` is provided, it retrieves the assistant using `_get_assistant_data_by_name`.
        - If neither parameter is provided, a `MissingRequirementException` is raised.

        :param assistant_id: str, optional - The unique identifier of the assistant.
        :param detail: str, optional - The level of detail for the response. Possible values:
           - "summary": Provides a summarized response. (Default)
           - "full": Provides detailed assistant data.
        :param assistant_name: str, optional - The name of the assistant.
        :raises MissingRequirementException: If neither `assistant_id` nor `assistant_name` is provided.
        :return: Assistant - The assistant details retrieved based on the provided identifier.
        """
        if not (assistant_id or assistant_name):
            raise MissingRequirementException("Either assistant_id or assistant_name must be defined to retrieve assistant data.")

        if assistant_id:
            return self._get_assistant_data_by_id(assistant_id=assistant_id, detail=detail)
        elif assistant_name:
            return self._get_assistant_data_by_name(assistant_name=assistant_name)

    def _get_assistant_data_by_id(
            self,
            assistant_id: str,
            detail: str = "summary"
    ) -> Assistant:
        """
        Retrieves detailed data for a specific assistant.

        This method calls `AssistantClient.get_assistant_data` to fetch assistant details
        and maps the response using `AssistantResponseMapper.map_to_assistant_list_response`.

        If the response contains errors, they are processed using `ErrorMapper` to return an `ErrorListResponse`.

        :param assistant_id: str - The unique identifier of the assistant to retrieve.
        :param detail: str, optional - The level of detail to include in the response. Possible values:
            - "summary": Provides a summarized response. (Default)
            - "full": Provides detailed assistant data.
        :return: AssistantResponse - The mapped response containing assistant details or an error list.
        """
        response_data = self.__assistant_client.get_assistant_data(
            assistant_id=assistant_id,
            detail=detail
        )
        if "errors" in response_data:
            result = ErrorMapper.map_to_error_list_response(response_data)
        else:
            result = AssistantResponseMapper.map_to_assistant_response(response_data)

        return result

    def _get_assistant_data_by_name(self, assistant_name: str) -> RAGAssistant:
        """
        Retrieves detailed data for a specific assistant by name.

        This method calls `RAGAssistantClient.get_assistant_data` to fetch assistant details
        and maps the response using `RAGAssistantMapper.map_to_rag_assistant`.

        If the response contains errors, they are processed using `ErrorMapper` to return an `ErrorListResponse`.

        :param assistant_name: str - The name of the assistant to retrieve.
        :return: RAGAssistant - The mapped response containing assistant details or an error list.
        """
        response_data = self.__rag_client.get_assistant_data(
            name=assistant_name
        )
        if "errors" in response_data:
            result = ErrorMapper.map_to_error_list_response(response_data)
        else:
            result = RAGAssistantMapper.map_to_rag_assistant(response_data)

        return result

    def create_assistant(
            self,
            assistant: Assistant
    ):
        """
        Creates a new assistant instance.

        This method checks if the provided assistant is an instance of `TextAssistant` or `ChatAssistant`.
        If so, it delegates the creation process to `_create_assistant`.

        :param assistant: Assistant - The assistant instance to be created.
        :return: The response from `_create_assistant`, which contains details of the created assistant.
        """
        if isinstance(assistant, TextAssistant) or isinstance(assistant, ChatAssistant):
            return self._create_chat_assistant(
                assistant
            )
        elif isinstance(assistant, RAGAssistant):
            return self._create_rag_assistant(
                assistant
            )

    def _create_chat_assistant(
            self,
            assistant: Assistant
    ) -> NewAssistantResponse:
        response_data = self.__assistant_client.create_assistant(
            assistant_type=assistant.type,
            name=assistant.name,
            prompt=assistant.prompt,
            description=assistant.description,
            llm_settings=assistant.llm_settings.to_dict(),
            welcome_data=assistant.welcome_data.to_dict()
        )
        if "errors" in response_data:
            result = ErrorMapper.map_to_error_list_response(response_data)
        else:
            result = AssistantResponseMapper.map_to_assistant_created_response(response_data)

        return result

    def _create_rag_assistant(
            self,
            assistant: RAGAssistant
    ) -> RAGAssistant:

        response_data = self.__rag_client.create_assistant(
            name=assistant.name,
            description=assistant.description,
            template=assistant.template,
            search_options=assistant.search_options.to_dict() if assistant.search_options else None,
            index_options=assistant.index_options.to_dict() if assistant.index_options else None,
            welcome_data=assistant.welcome_data.to_dict() if assistant.welcome_data else None
        )
        print(f"response_data: {response_data}")
        if "errors" in response_data:
            result = ErrorMapper.map_to_error_list_response(response_data)
        else:
            result = RAGAssistantMapper.map_to_rag_assistant(response_data)

        return result

    def update_assistant(
            self,
            assistant: Assistant,
            action: str = "saveNewRevision",
            revision_id: str = None
    ) -> Any:
        """
       Updates an assistant based on its type.

       This method determines the assistant type and delegates the update process accordingly:
       - Calls `_update_chat_assistant` for `TextAssistant` or `ChatAssistant`.
       - Calls `_update_rag_assistant` for `RAGAssistant`.

       :param assistant: Assistant - The assistant instance to be updated.
       :param action: str, optional - The type of update action for chat-based assistants. Options:
           - "save": Updates an existing revision (requires `revision_id`).
           - "saveNewRevision" (default): Creates and saves a new revision.
           - "savePublishNewRevision": Creates, saves, and publishes a new revision.
       :param revision_id: str, optional - The ID of the existing revision to update.
           Required if `action` is "save". Must be None for "saveNewRevision" or "savePublishNewRevision".
       :return: Any - The updated assistant instance or an error response if the update fails.
       :raises ValueError: If `action` is not a valid option.
       :raises MissingRequirementException:
           - If `action` is "save" and `revision_id` is not provided.
           - If `revision_id` is provided for "saveNewRevision" or "savePublishNewRevision".
       """
        if isinstance(assistant, TextAssistant) or isinstance(assistant, ChatAssistant):
            return self._update_chat_assistant(assistant=assistant, action=action, revision_id=revision_id)
        elif isinstance(assistant, RAGAssistant):
            return self._update_rag_assistant(assistant=assistant)

    def _update_chat_assistant(
            self,
            assistant: Assistant,
            action: str = "saveNewRevision",  # "save", "saveNewRevision", "savePublishNewRevision"
            revision_id: str = None
    ) -> NewAssistantResponse:
        """
        Updates an assistant with a specified action.

        This method calls `AssistantClient.update_assistant` to update the assistant and maps the response
        using `AssistantResponseMapper.map_to_assistant_created_response`.

        If the response contains errors, they are processed using `ErrorMapper` to return an `ErrorListResponse`.

        :param assistant: Assistant - The assistant instance containing updated details.
        :param action: str - The type of update action. Options:
            - "save": Updates an existing revision (requires `revision_id`).
            - "saveNewRevision": Creates and saves a new revision.
            - "savePublishNewRevision": Creates, saves, and publishes a new revision.
        :param revision_id: str, optional - The ID of the existing revision to update.
            Required if `action` is "save". Must be None for "saveNewRevision" or "savePublishNewRevision".
        :return: NewAssistantResponse - A response object containing the updated assistant details or an error list if the request fails.
        :raises ValueError: If `action` is not one of the valid options.
        :raises MissingRequirementException:
            - If `action` is "save" and `revision_id` is not provided.
            - If `revision_id` is provided for "saveNewRevision" or "savePublishNewRevision".
        """
        if action not in ["save", "saveNewRevision", "savePublishNewRevision"]:
            raise ValueError("Valid actions are: 'save', 'saveNewRevision', 'savePublishNewRevision'")

        if action == "save" and revision_id is None:
            raise MissingRequirementException(
                "revision_id is required if user needs to update an existent revision when action = save "
            )

        if revision_id is not None and (action == "saveNewRevision" or action == "savePublishNewRevision"):
            raise MissingRequirementException(
                "Assistant prompt is required if revisionId is specified or in case of actions saveNewRevision and savePublishNewRevision"
            )

        response_data = self.__assistant_client.update_assistant(
            assistant_id=assistant.id,
            status=assistant.status,
            action=action,
            revision_id=revision_id,
            name=assistant.name,
            prompt=assistant.prompt,
            description=assistant.description,
            llm_settings=assistant.llm_settings.to_dict(),
            welcome_data=assistant.welcome_data.to_dict()
        )

        if "errors" in response_data:
            result = ErrorMapper.map_to_error_list_response(response_data)
        else:
            result = AssistantResponseMapper.map_to_assistant_created_response(response_data)

        return result

    def _update_rag_assistant(
            self,
            assistant: RAGAssistant
    ) -> RAGAssistant:
        """
        Updates an existing RAGAssistant instance.

        This method calls `RAGAssistantClient.update_assistant` to update the assistant details and maps the response
        using `RAGAssistantMapper.map_to_rag_assistant`.

        If the response contains errors, they are processed using `ErrorMapper` to return an `ErrorListResponse`.

        :param assistant: RAGAssistant - The assistant instance containing updated details.
        :return: RAGAssistant - The updated RAGAssistant instance if the update is successful, or an error-mapped response if the request fails.
        :raises Exception: If the update request encounters unexpected errors.
        """
        response_data = self.__rag_client.update_assistant(
            name=assistant.name,
            status=assistant.status,
            description=assistant.description,
            template=assistant.template,
            search_options=assistant.search_options.to_dict() if assistant.search_options else None,
            welcome_data=assistant.welcome_data.to_dict() if assistant.welcome_data else None
        )
        if "errors" in response_data:
            result = ErrorMapper.map_to_error_list_response(response_data)
        else:
            result = RAGAssistantMapper.map_to_rag_assistant(response_data)

        return result

    def delete_assistant(
            self,
            assistant_id: str = None,
            assistant_name: str = None
    ) -> EmptyResponse:
        """
        Deletes an assistant using either an assistant ID or an assistant name.

        This method removes an assistant by calling either `_delete_assistant_by_id`
        or `_delete_assistant_by_name`, depending on the provided parameters.

        - If `assistant_id` is provided, it deletes the assistant using `_delete_assistant_by_id`.
        - If `assistant_name` is provided, it deletes the assistant using `_delete_assistant_by_name`.
        - If neither parameter is provided, a `MissingRequirementException` is raised.

        :param assistant_id: str, optional - The unique identifier of the assistant to delete.
        :param assistant_name: str, optional - The name of the assistant to delete.
        :raises MissingRequirementException: If neither `assistant_id` nor `assistant_name` is provided.
        :return: EmptyResponse - A response indicating success or an error list if the deletion fails.
        """
        if not (assistant_id or assistant_name):
            raise MissingRequirementException("Cannot delete assistant without either assistant_id or assistant_name")

        if assistant_id:
            return self._delete_assistant_by_id(assistant_id=assistant_id)
        elif assistant_name:
            return self._delete_assistant_by_name(assistant_name=assistant_name)

    def _delete_assistant_by_id(
            self,
            assistant_id: str,
    ) -> EmptyResponse:
        """
        Deletes an assistant by its unique identifier.

        This method calls `AssistantClient.delete_assistant` to remove an assistant and maps the response
        using `ResponseMapper.map_to_empty_response`.

        If the response contains errors, they are processed using `ErrorMapper` to return an `ErrorListResponse`.

        :param assistant_id: str - The unique identifier of the assistant to be deleted.
        :return: EmptyResponse - An empty response indicating successful deletion or an error list if the request fails.
        """
        response_data = self.__assistant_client.delete_assistant(
            assistant_id=assistant_id
        )
        if "errors" in response_data:
            result = ErrorMapper.map_to_error_list_response(response_data)
        else:
            result = ResponseMapper.map_to_empty_response(response_data)

        return result

    def _delete_assistant_by_name(
            self,
            assistant_name: str,
    ) -> EmptyResponse:
        """
        Deletes an assistant by its name.

        This method calls `RAGAssistantClient.delete_assistant` to remove the assistant
        and maps the response using `ResponseMapper.map_to_empty_response`.

        If the response contains errors, they are processed using `ErrorMapper` to return an `ErrorListResponse`.

        :param assistant_name: str - The name of the assistant to be deleted.
        :return: EmptyResponse - A response indicating success or an error list if the deletion fails.
        """
        response_data = self.__rag_client.delete_assistant(
            name=assistant_name
        )
        if "errors" in response_data:
            result = ErrorMapper.map_to_error_list_response(response_data)
        else:
            result = ResponseMapper.map_to_empty_response(response_data)

        return result

    def send_chat_request(
            self,
            assistant: Assistant,
            messages: ChatMessageList,
            revision: AssistantRevision = None,
            variables: ChatVariableList = None
    ) -> ChatResponse:
        """
        Sends a chat request to the assistant and processes the response.

        This method sends a conversation request to an AI assistant, including a list of chat messages,
        an optional revision identifier, and optional chat variables. It then maps the response to
        either an error list or a structured chat response.

        :param assistant: Assistant - The assistant instance handling the request.
        :param messages: ChatMessageList - The list of messages forming the chat history.
        :param revision: AssistantRevision, optional - The assistant revision details (default: None).
        :param variables: ChatVariableList, optional - Additional variables for the chat request (default: None).

        :return: ChatResponse - The structured response from the assistant, either a chat response
                 or an error list.
        """
        response_data = self.__assistant_client.send_chat_request(
            assistant_name=assistant.name,
            messages=messages.to_list(),
            revision=revision.revision_id if revision is not None else None,
            revision_name=revision.revision_name if revision is not None else None,
            variables=variables.to_list() if variables else None
        )
        if "errors" in response_data:
            result = ErrorMapper.map_to_error_list_response(response_data)
        else:
            result = AssistantResponseMapper.map_to_chat_request_response(response_data)

        return result

    def get_request_status(self, request_id: str) -> ChatResponse:
        """
        Retrieves the status of a chat request using the provided request ID.

        This method queries the assistant service to check the current status of a
        previously sent chat request. It then processes the response, mapping it to either
        a structured chat response or an error list if any issues are found.

        :param request_id: str - The unique identifier of the chat request.

        :return: ChatResponse - The structured response containing the request status, or
                 an error list if the request failed.
        """
        response_data = self.__assistant_client.get_request_status(
            request_id=request_id
        )
        if "errors" in response_data:
            result = ErrorMapper.map_to_error_list_response(response_data)
        else:
            result = AssistantResponseMapper.map_to_chat_request_response(response_data)

        return result

    def cancel_request(self, request_id: str) -> ChatResponse:
        """
        Cancels an ongoing chat request using the provided request ID.

        This method sends a cancellation request to the assistant service. If the request
        is successfully canceled, it returns a structured chat response. If there are
        errors, it maps them to an error list response.

        :param request_id: str - The unique identifier of the chat request to cancel.

        :return: ChatResponse - The structured response confirming the cancellation,
                 or an error list if the cancellation fails.
        """
        response_data = self.__assistant_client.cancel_request(
            request_id=request_id
        )
        if "errors" in response_data:
            result = ErrorMapper.map_to_error_list_response(response_data)
        else:
            result = AssistantResponseMapper.map_to_chat_request_response(response_data)

        return result

    def chat_completion(
            self,
            model: str,
            messages: ChatMessageList,
            llm_settings: LlmSettings,
            thread_id: str = None,
            variables: ChatVariableList = None
    ):
        """
        Generates a chat completion response using the specified language model.

        This method sends a chat completion request to the ChatClient with the provided
        model, messages, and settings. It processes the response by mapping errors if
        present or converting it into an assistant response format.

        :param model: str - The identifier of the language model to use.
        :param messages: ChatMessageList - A list of chat messages to provide context for the completion.
        :param llm_settings: LlmSettings - Configuration settings for the language model,
                             including temperature, max tokens, and penalties.
        :param thread_id: str, optional - An optional identifier for the conversation thread.
        :param variables: ChatVariableList, optional - Additional variables to include in the request.

        :return: ChatResponse - The structured chat response if successful,
                 or an error list if an issue occurs.
        """
        response_data = self.__chat_client.chat_completion(
            model=model,
            messages=messages.to_list(),
            stream=False,
            temperature=llm_settings.temperature,
            max_tokens=llm_settings.max_tokens,
            thread_id=thread_id,
            frequency_penalty=llm_settings.frequency_penalty,
            presence_penalty=llm_settings.presence_penalty,
            variables=variables
        )

        if "errors" in response_data:
            result = ErrorMapper.map_to_error_list_response(response_data)
        else:
            result = AssistantResponseMapper.map_to_chat_request_response(response_data)

        return result

    def get_document_list(
            self,
            name: str,
            skip: int = 0,
            count: int = 10
    ) -> DocumentListResponse:
        """
        Retrieves a list of documents associated with a specified RAG assistant.

        :param name: str - The name of the RAG assistant.
        :param skip: int - The number of documents to skip (default: 0).
        :param count: int - The number of documents to retrieve (default: 10).

        :return: DocumentListResponse - A response object containing the retrieved documents or an error response.

        :raises Exception: If the API call encounters errors, they will be mapped using ErrorMapper.
        """
        response_data = self.__rag_client.get_documents(
            name=name,
            skip=skip,
            count=count
        )

        if "errors" in response_data:
            result = ErrorMapper.map_to_error_list_response(response_data)
        else:
            result = RAGAssistantMapper.map_to_document_list_response(response_data)

        return result

    def delete_all_documents(
            self,
            name: str,
    ) -> EmptyResponse:
        """
        Deletes all documents associated with a specified RAG assistant.

        :param name: str - The name of the RAG assistant whose documents should be deleted.

        :return: EmptyResponse - A response object indicating the success or failure of the operation.

        :raises Exception: If the API call encounters errors, they will be mapped using ErrorMapper.
        """
        response_data = self.__rag_client.delete_all_documents(
            name=name
        )

        if "errors" in response_data:
            result = ErrorMapper.map_to_error_list_response(response_data)
        else:
            result = ResponseMapper.map_to_empty_response(response_data)

        return result

    def get_document(
            self,
            name: str,
            document_id: str
    ) -> Document:
        """
        Retrieves a specific document associated with a RAG assistant.

        :param name: str - The name of the RAG assistant.
        :param document_id: str - The unique identifier of the document to retrieve.

        :return: DocumentResponse - A response object containing the retrieved document or an error response.

        :raises Exception: If the API call encounters errors, they will be mapped using ErrorMapper.
        """
        response_data = self.__rag_client.retrieve_document(
            name=name,
            document_id=document_id
        )

        if "errors" in response_data:
            result = ErrorMapper.map_to_error_list_response(response_data)
        else:
            result = RAGAssistantMapper.map_to_document(response_data)

        return result

    def upload_document(
            self,
            assistant: RAGAssistant,
            document: UploadDocument
    ) -> Document:
        """
        Uploads a document to the specified RAG assistant.

        :param assistant: RAGAssistant - The assistant to which the document will be uploaded.
        :param document: UploadDocument - The document object containing:
            - path (str): The file path of the document.
            - upload_type (str): The type of upload (e.g., "multipart" or "binary").
            - metadata (dict | str | None): Additional metadata, either as a dictionary or a file path.
            - content_type (str): The MIME type of the document (e.g., "application/pdf", "text/plain").

        :return: Document - The uploaded document instance.

        :raises ValueError: If an error occurs during the upload, it is mapped using ErrorMapper.
        """
        response_data = self.__rag_client.upload_document(
            name=assistant.name,
            file_path=document.path,
            upload_type=document.upload_type,
            metadata=document.metadata,
            content_type=document.content_type
        )

        if "errors" in response_data:
            result = ErrorMapper.map_to_error_list_response(response_data)
        else:
            result = RAGAssistantMapper.map_to_document(response_data)

        return result

    def delete_document(
            self,
            name: str,
            document_id: str
    ) -> EmptyResponse:
        """
        Deletes a specific document from the given RAG assistant.

        :param name: str - The name of the RAG assistant from which the document will be deleted.
        :param document_id: str - The unique identifier of the document to be deleted.

        :return: EmptyResponse - An empty response object indicating success or failure.

        :raises ValueError: If an error occurs during deletion, it is mapped using ErrorMapper.
        """
        response_data = self.__rag_client.delete_document(
            name=name,
            document_id=document_id
        )

        if "errors" in response_data:
            result = ErrorMapper.map_to_error_list_response(response_data)
        else:
            result = ResponseMapper.map_to_empty_response(response_data)

        return result
