from deepkeep._exceptions import DeepkeepError
from ..base_module import BaseModule

__all__ = ["Chat"]


class Chat(BaseModule):
    root_path: str = "monitoring"

    def create(self, host_id: str = BaseModule._DEFAULT_HOST_):
        return self._make_request(method="POST", path=f"{self.root_path}/{host_id}/chat")

    def delete(self, host_id: str = BaseModule._DEFAULT_HOST_):
        return self._make_request(method="DELETE", path=f"{self.root_path}/{host_id}/chat")

    def get(self, host_id: str = BaseModule._DEFAULT_HOST_):
        return self._make_request(path=f"{self.root_path}/{host_id}/chat")

    def statistics(self, host_id: str = BaseModule._DEFAULT_HOST_):
        return self._make_request(path=f"report/statistics/chat/{host_id}")

    def status(self, host_id: str = BaseModule._DEFAULT_HOST_):
        return self._make_request(path=f"{self.root_path}/{host_id}/status")
