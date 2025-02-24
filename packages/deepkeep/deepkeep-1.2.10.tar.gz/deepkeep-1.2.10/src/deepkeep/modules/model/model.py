from typing import Optional
from ..base_module import BaseModule
from deepkeep.modules.integrations.consts import IntegrationsType
from .utils import arrange_locals


class Model(BaseModule):
    root_path: str = "model"

    def __init__(self, client: 'DeepKeep'):
        super().__init__(client)
        self.package = 'deepkeep.modules.model.integration_models'
        self._modules = [integration_model.value for integration_model in IntegrationsType]
        self._load_modules()

    def create(self, title: str, model_framework: str, model_purpose: str, description: str = "Default description",
               model_source_path: str = None, source_type: str = "local", loading_option: str = "other",
               training_params: dict = None,
               requirements: list[str] = None, input_categories: list[dict] = None,
               output_categories: list[dict] = None,
               **kwargs):
        """
        Create a new model metadata object and save it to the metadata repository.
        :param title: Name of the model.
        :param model_framework: Framework used by the model. (Required)
        :param model_purpose: Purpose of the model. (Required)
        :param description: Description of the model.
        :param model_source_path: Path to where the model's data is stored.
        :param source_type: Type of source used to store the model. (Default: local)
        :param loading_option: How to load the model. (Default: framework)
        :param training_params: Training parameters.
        :param requirements: Requirements list for the model.
        :param input_categories: A list of dicts containing the name, type and shape of the inputs to the model.
        :param output_categories: A list of dicts containing the name, type and shape of the outputs of the model.
        :param kwargs: Optional additional keyword arguments:
           - model_loading_path: Path to the model loading file if LoadingOption is CODE
           - class_mapping: Class mapping for the model, in case of classification/object detection models.
        :return: Created model ID.
        """
        data = arrange_locals(locals(), filter_none=False)

        # In case of integration model - map to the right module, and extract kwargs as other parameters
        if "integration_id" in data["kwargs"]:
            integration_source = self._client.integrations.get(data["kwargs"]["integration_id"]).get("source")
            integration_model = getattr(self, integration_source.lower(), f"Module '{integration_source}' not found!")
            data.update(data.pop('kwargs'))
            # create new integration model
            return integration_model.create(**data)

        return self._make_request(method="POST", path=f"{self.root_path}/", json_params=data)

    def get(self, model_id: str) -> dict:
        """
        Get model metadata by model ID.
        :param model_id: string representing the model ID
        :return: dict with model metadata
        """
        return self._make_request(method="GET", path=f"{self.root_path}/{model_id}")

    def get_by_title(self, model_title: str) -> Optional[dict]:
        """
        Get model metadata by model title.
        :param model_title: string representing the model title
        :return: dict with model metadata
        """
        search_query = {"query": [{"field": "title.keyword",
                                   "operator": "equals",
                                   "value": model_title}],
                        "sort": [{"field": "created_time",
                                  "direction": "desc"}]}
        models_meta = self._make_request(method="GET", path=f"{self.root_path}/", json_params=search_query)
        return models_meta[0] if models_meta else None

    def update(self, model_id: str, status: str = None, title: str = None, description: str = None,
               tags: list[str] = None) -> bool:
        """
        Update model metadata by model ID.
        :param model_id: string representing the model ID
        :param status: string representing the status of the model
        :param title: string representing the title of the model
        :param description: string representing the description of the model
        :param tags: list of tags related to the model
        :return: True if the update ended successfully, False otherwise
        """
        data = arrange_locals(locals(), ["model_id"])
        return self._make_request(method="PUT", path=f"{self.root_path}/{model_id}",
                                  json_params=data)

    def delete(self, model_id: str) -> bool:
        """
        Delete model metadata by model ID.
        :param model_id: string representing the model ID
        :return: True if delete ended successfully, False otherwise
        """
        return self._make_request(method="DELETE", path=f"{self.root_path}/{model_id}")
