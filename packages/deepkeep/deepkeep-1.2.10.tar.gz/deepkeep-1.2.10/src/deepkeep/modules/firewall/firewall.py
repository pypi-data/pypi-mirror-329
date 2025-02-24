from ..base_module import BaseModule
from .filter import Filter


class Firewall(BaseModule):
    root_path: str = "firewall"
    filter: Filter

    def __init__(self, client: 'DeepKeep'):
        super().__init__(client)
        self.filter = Filter(self._client)

    def create(self, model_id: str, name: str, description: str = None, dataset_id: str = None,
               blank: bool = True, application_id: str = "") -> dict:
        """
        Create a new firewall
        :param model_id: model id that the firewall is related to
        :param name: firewall name
        :param description: firewall description
        :param dataset_id: dataset id that the firewall is related to
        :param blank: bool: Determines whether to create a blank firewall.
                    - True (default), the firewall will be created without any processes-filters (blank).
                    - False, the firewall will be created with all optional processes that align with the model's purpose.
        :param application_id: application id that the firewall is related to
        :return: dict with firewall creation response
        """
        return self._make_request(method="POST", path=f"{self.root_path}/",
                                  json_params={
                                      "name": name,
                                      "description": description,
                                      "model_id": model_id,
                                      "dataset_id": dataset_id,
                                      "blank": blank,
                                      "application_id": application_id})

    def update(self, firewall_id: str, name: str = None, description: str = None, status: str = None) -> dict:
        """
        Update firewall details
        :param firewall_id: id of the firewall to update
        :param name: new name
        :param description: new description
        :param status: new status
        :return: dict with update response
        """
        json_params = {key: value for key, value in {"name": name, "description": description, "status": status}.items()
                       if value is not None}
        return self._make_request(method="PUT", path=f"{self.root_path}/{firewall_id}", json_params=json_params)

    def activate(self, firewall_id: str) -> dict:
        """
        Activate a firewall
        :param firewall_id: str: firewall id to activate
        :return: dict with activation response
        """
        return self._make_request(method="POST", path=f"{self.root_path}/{firewall_id}/activate")

    def delete(self, firewall_id: str) -> bool:
        """
        Delete a firewall
        :param firewall_id: str: firewall id to delete
        return True if delete succeeded, and False otherwise.
        """
        return self._make_request(method="DELETE", path=f"{self.root_path}/{firewall_id}")


