from deepkeep.modules.model.model import Model, arrange_locals
from deepkeep.modules.integrations.consts import IntegrationsType
from deepkeep.modules.base_module import BaseModule
from deepkeep.modules.model.utils import pop_keys_from_dict


class AzureOpenAI(BaseModule):
    source = IntegrationsType.Azure_OpenAI.value

    def create(self, title: str, model_framework: str, model_purpose: str, description: str = "Default description",
               model_source_path: str = None, source_type: str = "local", loading_option: str = "other",
               integration_id: str = None, integration_model_name: str = None, training_params: dict = None,
               requirements: list[str] = None, input_categories: list[dict] = None,
               output_categories: list[dict] = None, max_tokens: int = 100, temperature: float = 0.5, **kwargs):
        """
        Create a new model with azure openai integration.
        :param title: Name of the model.
        :param model_framework: Framework used by the model. (Required)
        :param model_purpose: Purpose of the model. (Required)
        :param description: Description of the model.
        :param model_source_path: Path to where the model's data is stored.
        :param source_type: Type of source used to store the model. (Default: local)
        :param loading_option: How to load the model. (Default: framework)
        :param integration_id: integration ID model is related to
        :param integration_model_name: model name from integration model is related to
        :param training_params: Training parameters.
        :param requirements: Requirements list for the model.
        :param input_categories: A list of dicts containing the name, type and shape of the inputs to the model.
        :param output_categories: A list of dicts containing the name, type and shape of the outputs of the model.
        :param max_tokens: max tokens for integration model
        :param temperature: integration models temperature
        :param kwargs: Optional additional keyword arguments:
           - model_loading_path: Path to the model loading file if LoadingOption is CODE
           - class_mapping: Class mapping for the model, in case of classification/object detection models.
        :return: The response from the API.
        """
        data, initialize_data = pop_keys_from_dict(arrange_locals(locals()), ["max_tokens", "temperature"])
        data["initialize_data"] = initialize_data
        try:
            return self._make_request(method="POST", path=Model.root_path, json_params=data)
        except Exception as e:
            raise Exception(f"failed to create new model with {self.source} integration due to: {e}")
