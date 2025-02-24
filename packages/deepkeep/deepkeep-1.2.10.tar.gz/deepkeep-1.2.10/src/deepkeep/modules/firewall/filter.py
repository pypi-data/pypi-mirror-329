from ..base_module import BaseModule
from .templates import Templates


class Filter(BaseModule):
    root_path: str = "firewall"
    templates: Templates

    def __init__(self, client: 'DeepKeep'):
        super().__init__(client)
        self.templates = Templates(self._client)

    def add(self, firewall_id: str, filter_option_id: str, direction: str = "request",
            override_filters: bool = False):
        """
        Add a filter to a firewall
        :param firewall_id: str: firewall id
        :param filter_option_id: str: filter option id
        :param direction: str: direction of the filter (request/response), will be used in case of process that fits
        'both' directions
        :param override_filters: bool, indicates whether to clear the previous filters from the firewall.
        :return: dict: response
        """
        return self._make_request(method="POST", path=f"{self.root_path}/{firewall_id}/filter/{filter_option_id}",
                                  json_params={"direction": direction,
                                               "override_filters": override_filters})

    def get_configuration(self, firewall_id: str, filter_id: str):
        """
        Get configuration for a filter in the firewall
        :param firewall_id: str: firewall id
        :param filter_id: str: filter id
        :return: dict with filter's configuration
        """
        return self._make_request(method="GET", path=f"{self.root_path}/{firewall_id}/filter/{filter_id}/configuration")

    def set_configuration(self, firewall_id: str, filter_id: str, data: dict):
        """
        Set configuration for a filter in the firewall
        :param firewall_id: str: firewall id
        :param filter_id: str: filter id
        :param data: dict: updated configuration
        :return: update response
        """
        updated_configuration = {"data": data}
        return self._make_request(method="POST",
                                  path=f"{self.root_path}/{firewall_id}/filter/{filter_id}/configuration",
                                  json_params=updated_configuration)
