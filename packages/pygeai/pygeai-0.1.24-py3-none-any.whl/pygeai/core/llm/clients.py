import json

from pygeai.core.base.clients import BaseClient
from pygeai.core.llm.endpoints import GET_PROVIDER_LIST_V2, GET_PROVIDER_DATA_V2, GET_PROVIDER_MODELS_V2, \
    GET_MODEL_DATA_V2


class LlmClient(BaseClient):

    def get_provider_list(self) -> dict:
        response = self.api_service.get(endpoint=GET_PROVIDER_LIST_V2)
        result = json.loads(response.content)
        return result

    def get_provider_data(self, provider_name: str) -> dict:
        endpoint = GET_PROVIDER_DATA_V2.format(providerName=provider_name)
        response = self.api_service.get(endpoint=endpoint)
        result = json.loads(response.content)
        return result

    def get_provider_models(self, provider_name: str) -> dict:
        endpoint = GET_PROVIDER_MODELS_V2.format(providerName=provider_name)
        response = self.api_service.get(endpoint=endpoint)
        result = json.loads(response.content)
        return result

    def get_model_data(
            self,
            provider_name: str,
            model_name: str = None,
            model_id: str = None
    ) -> dict:
        endpoint = GET_MODEL_DATA_V2.format(
            providerName=provider_name,
            modelNameOrId=model_name or model_id
        )
        response = self.api_service.get(endpoint=endpoint)
        result = json.loads(response.content)
        return result




