from ..base_module import BaseModule
from .topic_option import TopicOption


def get_root_path(evaluation_id: str) -> str:
    return f"evaluation/{evaluation_id}/topic"


# topic = process instance


class Topic(BaseModule):
    topics_options: TopicOption
    root_path = get_root_path("evaluation_id")

    def __init__(self, client: 'DeepKeep'):
        super().__init__(client)
        self.topics_options = TopicOption(self._client)

    def add(self, evaluation_id: str, topic_option_id: str):
        return self._make_request(method="POST", path=f"{get_root_path(evaluation_id)}/{topic_option_id}")

    def get(self, evaluation_id: str, topic_id: str = None):
        if topic_id:
            return self._make_request(method="GET", path=f"{get_root_path(evaluation_id)}/{topic_id}")
        return self._make_request(method="GET", path=f"{get_root_path(evaluation_id)}/topics")

    def delete(self, evaluation_id: str, topic_id: str):
        return self._make_request(method="DELETE", path=f"{get_root_path(evaluation_id)}/{topic_id}")

    def get_topic_configuration(self, evaluation_id: str, topic_id: str):
        return self._make_request(method="GET", path=f"{get_root_path(evaluation_id)}/{topic_id}/configuration")

    def set_topic_configuration(self, evaluation_id: str, topic_id: str, data: dict):
        updated_data = {"data": data}
        return self._make_request(method="POST", path=f"{get_root_path(evaluation_id)}/{topic_id}/configuration",
                                  json_params=updated_data)
