from deepkeep.modules.integrations.integrations import Integrations
from deepkeep.modules.integrations.consts import IntegrationsType
from deepkeep.modules.base_module import BaseModule


class AzureOpenAI(BaseModule):
    source = IntegrationsType.Azure_OpenAI.value

    def create(self, name: str, token: str, api_version: str, host: str):
        data = {"name": name, "token": token, "source": self.source, "setup_params": {"api_version": api_version,
                                                                                      "host": host}}
        try:
            return self._make_request(method="POST", path=f"{Integrations.root_path}/", json_params=data)
        except Exception as e:
            raise Exception(f"failed to create {self.source} integration due to: {e}")

    def update(self, integration_id: str, name: str = None, api_version: str = None, host: str = None,
               token: str = None):
        setup_params = {key: value for key, value in {"api_version": api_version, "host": host}.items() if value}
        data = {key: value for key, value in {"name": name, "token": token, "setup_params": setup_params}.items() if value}
        try:
            return self._make_request(method="PUT", path=f"{Integrations.root_path}/{integration_id}", json_params=data)
        except Exception as e:
            raise Exception(f"failed to update integration with ID:{integration_id} due to: {e}")
