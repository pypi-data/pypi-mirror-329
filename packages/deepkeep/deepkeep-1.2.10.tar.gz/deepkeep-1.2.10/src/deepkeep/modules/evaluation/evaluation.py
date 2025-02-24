from ..base_module import BaseModule
from .topic import Topic
from .report import Report


__all__ = ["Evaluation"]


class Evaluation(BaseModule):
    root_path: str = "evaluation"
    topic: Topic

    def __init__(self, client: 'DeepKeep'):
        super().__init__(client)
        self.topic = Topic(self._client)
        self.report = Report(self._client)

    def create(self, model_id: str, name: str, application_id: str,
               description: str = None, dataset_id: str = None, blank: bool = True,):
        json_params = {
            "name": name,
            "model_id": model_id,
            "dataset_id": dataset_id,
            "blank": blank,
            "application_id": application_id,
            "description": description}
        data = self._make_request(method="POST", path=f"{self.root_path}/",
                                  json_params=json_params)
        return data

    def get(self, evaluation_id: str):
        return self._make_request(method="GET", path=f"{self.root_path}/{evaluation_id}")

    def update(self, evaluation_id: str, name: str = None, description: str = None, status: str = None):
        json_params = {param_name: param_value for param_name, param_value in [
            ("name", name), ("description", description), ("status", status)] if param_value}
        return self._make_request(method="PUT", path=f"{self.root_path}/{evaluation_id}",
                                  json_params=json_params)

    def delete(self, evaluation_id: str):
        return self._make_request(method="DELETE", path=f"{self.root_path}/{evaluation_id}")

    def list(self, filter_by: dict = None):
        return self._make_request(method="GET", path=f"{self.root_path}/evaluations", query_params=filter_by)

    def run(self, evaluation_id: str):
        return self._make_request(method="POST", path=f"{self.root_path}/{evaluation_id}/run")

