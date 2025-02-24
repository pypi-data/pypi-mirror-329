from ..base_module import BaseModule


class Report(BaseModule):
    root_path: str = "report"

    def statistics(self, user_id: str | None = None):
        return self._make_request(path=f"{self.root_path}/statistics/user/{user_id if user_id else ''}")
