from ..base_module import BaseModule


class Templates(BaseModule):
    root_path: str = "firewall"

    def get(self, firewall_id: str, query: dict | list[dict] = None):
        """
        Get optional filter templates for a firewall
        :param firewall_id: the ID of the firewall to fetch all optional filters for.
        :param query: Optional query to search filters by
        """
        return self._make_request(method="GET", path=f"{self.root_path}/{firewall_id}/filter_options",
                                  json_params=query if query else {})
