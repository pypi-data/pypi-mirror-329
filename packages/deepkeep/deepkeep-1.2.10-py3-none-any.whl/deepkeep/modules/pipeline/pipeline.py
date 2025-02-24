from typing import Union
from ..base_module import BaseModule


class Pipeline(BaseModule):
    root_path: str = "monitoring"

    def get(self, name: Union[str, None] = None, status: Union[str] = "running"):
        query_params = {key: value for key, value in locals().items() if
                        value and isinstance(value, BaseModule.PREMITIVE)}

        return self._make_request(path=f"{self.root_path}/", query_params=query_params)
