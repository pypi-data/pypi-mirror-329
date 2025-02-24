from ..base_module import BaseModule
from .consts import IntegrationsType


class Integrations(BaseModule):
    root_path: str = "integration"

    def __init__(self, client: 'DeepKeep'):
        super().__init__(client)
        self.package = 'deepkeep.modules.integrations.integrations_sources'
        self._modules = [integration_type.value for integration_type in IntegrationsType]
        self._load_modules()

    def get(self, integration_id: str):
        return self._make_request(method="GET", path=f"{self.root_path}/{integration_id}")

    def fetch_all(self, page: int = 1, size: int = 10):
        return self._make_request(method="GET", path=f"{self.root_path}/", query_params={"page": page, "size": size})

    def delete(self, integration_id: str):
        return self._make_request(method="DELETE", path=f"{self.root_path}/{integration_id}")

    def create(self, integration_name: str, integration_parameters: dict):
        """
        Create new integration, mapping to the right integration by integration name
        """
        integration_module = getattr(self, integration_name.lower(), f"Module '{integration_name}' not found!")
        return integration_module.create(**integration_parameters)
