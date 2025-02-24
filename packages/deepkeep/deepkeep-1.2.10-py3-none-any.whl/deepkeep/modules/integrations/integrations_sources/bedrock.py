from deepkeep.modules.base_module import BaseModule
from deepkeep.modules.integrations.integrations import Integrations
from deepkeep.modules.integrations.consts import IntegrationsType


class Bedrock(BaseModule):
    source = IntegrationsType.Bedrock.value

    def create(self, name: str, region_name: str, aws_access_key_id: str, aws_secret_access_key: str,
               connect_path: str = None):
        token = {'aws_access_key_id': aws_access_key_id,
                 'aws_secret_access_key': aws_secret_access_key}
        data = {"name": name, "token": token, "source": self.source, "setup_params": {"region_name": region_name}}

        if connect_path:
            data.update({'connect_path': connect_path})
            data['setup_params']['connect_path'] = connect_path
        try:
            return self._make_request(method="POST", path=f"{Integrations.root_path}/", json_params=data)
        except Exception as e:
            raise Exception(f"Failed to create {self.source} integration due to: {e}")

    def update(self, integration_id: str, name: str = None, region_name: str = None, aws_access_key: str = None,
               aws_access_secret_key: str = None, connect_path: str = None):
        data = {"name": name} if name else {}
        if aws_access_key and not aws_access_secret_key or aws_access_secret_key and not aws_access_key:
            raise ValueError("Both AWS access key and AWS secret key must be provided together")
        if aws_access_key and aws_access_secret_key:
            token = {'aws_access_key': aws_access_key, 'aws_access_secret_key': aws_access_secret_key}
            data['token'] = token
        if region_name:
            data.update({'setup_params': {'region_name': region_name}})
        if connect_path:
            data.update({'setup_params': {'connect_path': connect_path}})
        try:
            return self._make_request(method="PUT", path=f"{Integrations.root_path}/{integration_id}", json_params=data)
        except Exception as e:
            raise Exception(f"failed to update integration with ID:{integration_id} due to: {e}")
