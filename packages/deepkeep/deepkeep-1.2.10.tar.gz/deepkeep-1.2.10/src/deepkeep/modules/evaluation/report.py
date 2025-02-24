from ..base_module import BaseModule


def get_root_path(evaluation_id: str) -> str:
    return f"evaluation/{evaluation_id}/report"


# report = project run
# report_topic = process run


class Report(BaseModule):
    root_path = get_root_path("evaluation_id")

    def get_report_summary(self, evaluation_id: str, report_id: str):
        return self._make_request(method="GET", path=f"{get_root_path(evaluation_id)}/{report_id}")

    def get_report_topic(self, evaluation_id: str, report_id: str, report_topic_id: str):
        return self._make_request(method="GET", path=f"{get_root_path(evaluation_id)}/{report_id}/topic/{report_topic_id}")

    def list(self, evaluation_id: str, filter_by: dict = None):
        return self._make_request(method="GET", path=f"evaluation/{evaluation_id}/reports", query_params=filter_by)



