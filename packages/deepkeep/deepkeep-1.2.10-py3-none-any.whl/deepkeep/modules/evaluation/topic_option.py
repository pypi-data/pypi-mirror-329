from ..base_module import BaseModule


def get_root_path(evaluation_id: str) -> str:
    return f"evaluation/{evaluation_id}/topics_options"

# topic_option = process


class TopicOption(BaseModule):
    root_path: str = get_root_path("evaluation_id")

    def get(self, evaluation_id: str):
        return self._make_request(method="GET", path=get_root_path(evaluation_id))
