import json

from pygeai.chat.endpoints import CHAT_V1, CHAT_COMPLETION_V1
from pygeai.core.base.clients import BaseClient


class ChatClient(BaseClient):

    def chat(self):
        response = self.api_service.post(
            endpoint=CHAT_V1
        )
        result = json.loads(response.content)
        return result

    def chat_completion(
            self,
            model: str,
            messages: list,
            stream: bool = False,
            temperature: int = None,
            max_tokens: int = None,
            thread_id: str = None,
            frequency_penalty: float = None,
            presence_penalty: float = None,
            variables: list = None
    ) -> dict:
        """
        Generates a chat completion response using the specified model and parameters.

        :param model: str - The model specification in the format
            "saia:<assistant_type>:<assistant_name>|<bot_id>". Determines the assistant type and associated configuration. (Required)
        :param messages: list - A list of messages to include in the chat completion. Each message should be a dictionary with
            the following structure:
                {
                    "role": "string",  # Possible values: "user", "system", or others supported by the model
                    "content": "string"  # The content of the message
                } (Required)
        :param stream: bool - Whether the response should be streamed. Possible values:
            - False: Do not stream the response (default).
            - True: Stream the response.
        :param temperature: int - Controls the randomness of the response. Higher values (e.g., 2) produce more random responses,
            while lower values (e.g., 0.2) produce more deterministic responses. (Optional)
        :param max_tokens: int - The maximum number of tokens to generate in the response. (Optional)
        :param thread_id: str - An optional UUID to identify the conversation thread. (Optional)
        :param frequency_penalty: float - A value between -2.0 and 2.0. Positive values decrease the model's likelihood of
            repeating tokens based on their frequency in the text so far. (Optional)
        :param presence_penalty: float - A value between -2.0 and 2.0. Positive values increase the model's likelihood of
            discussing new topics by penalizing tokens that have already appeared in the text. (Optional)
        :param variables: list - A list of additional variables. These must be defined at the time of creation, otherwise
            its use will throw an error.
        :return: dict - The API response containing the chat completion result.
        """
        data = {
            'model': model,
            'messages': messages,
            'stream': stream
        }
        if temperature:
            data['temperature'] = temperature

        if max_tokens:
            # TODO -> Review deprecation of max_tokens in favor of max_completion_tokens
            data['max_tokens'] = max_tokens

        if thread_id:
            data['threadId'] = thread_id

        if frequency_penalty:
            data['frequency_penalty'] = frequency_penalty

        if presence_penalty:
            data['presence_penalty'] = presence_penalty

        if variables is not None and any(variables):
            data['variables'] = variables

        response = self.api_service.post(
            endpoint=CHAT_COMPLETION_V1,
            data=data
        )
        result = json.loads(response.content)
        return result

