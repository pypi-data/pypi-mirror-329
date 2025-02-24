from deepkeep.modules.model.model import Model, arrange_locals
from deepkeep.modules.integrations.consts import IntegrationsType
from deepkeep.modules.base_module import BaseModule
from deepkeep.modules.model.utils import pop_keys_from_dict


class Bedrock(BaseModule):
    source = IntegrationsType.Bedrock.value

    def create(self, title: str, model_framework: str, model_purpose: str, description: str = "Default description",
               model_source_path: str = None, source_type: str = "local", loading_option: str = "other",
               integration_id: str = None, integration_model_name: str = None, training_params: dict = None,
               requirements: list[str] = None, input_categories: list[dict] = None,
               output_categories: list[dict] = None, temperature: float = 0.5,
               top_p: float = 0.9, max_gen_len: int = 512, model_name: str = "meta.llama3-70b-instruct-v1:0",  **kwargs):
        """
        Create a new model with openai integration.
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
        :param temperature: integration model's temperature (default: 0.5)
        :param top_p: integration model's top_p value (default: 0.9)
        :param max_gen_len: integration model's maximum generation length (default: 512)
        :param model_name: The model name used for the integration (default: meta.llama3-70b-instruct-v1:0)
        :param kwargs: Optional additional keyword arguments:
        :return: The response from the API.
        """

        data, initialize_data = pop_keys_from_dict(arrange_locals(locals()),
                                                   ["max_tokens", "temperature", "infer_path", "connect_path", "top_p",
                                                    "max_gen_len", "model_name"])

        data["initialize_data"] = initialize_data
        try:
            return self._make_request(method="POST", path=Model.root_path, json_params=data)
        except Exception as e:
            raise Exception(f"failed to create new model with {self.source} integration due to: {e}")
