from dataclasses import dataclass
from typing import Union

from ..base_module import BaseModule, BaseData
from .message import validate_message_content

__all__ = ["Conversation"]


@dataclass
class ConversationData(BaseData):
    title: str = "New Chat"
    user_name: Union[str, None] = None
    system_prompt: Union[str, None] = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class Conversation(BaseModule):
    root_path: str = "monitoring"

    def create(self, user_id: str, host_id: str = BaseModule._DEFAULT_HOST_,
               data: Union[ConversationData, dict, None] = None, **kwargs):
        if not data or isinstance(data, dict):
            data = kwargs | (data or {})
            data = ConversationData(**data)

        return self._make_request(method="POST", path=f"{self.root_path}/{host_id}/conversation",
                                  headers={"user": user_id}, json_params=data.as_dict())

    def get(self, conversation_id: str, host_id: str = BaseModule._DEFAULT_HOST_):
        return self._make_request(path=f"{self.root_path}/{host_id}/conversation/{conversation_id}")

    def delete(self, conversation_id: str, host_id: str = BaseModule._DEFAULT_HOST_):
        return self._make_request(method="DELETE", path=f"{self.root_path}/{host_id}/conversation/{conversation_id}")

    def update(self, conversation_id: str, data: Union[ConversationData, dict],
               host_id: str = BaseModule._DEFAULT_HOST_):
        data = data or ConversationData()
        if isinstance(data, dict):
            data = ConversationData(**data)

        return self._make_request(method="PUT", path=f"{self.root_path}/{host_id}/conversation/{conversation_id}",
                                  json_params=data.as_dict())

    def statistics(self, conversation_id: str):
        return self._make_request(path=f"report/statistics/conversation/{conversation_id}")

    def check_user_input(self, conversation_id: str, prompt: str, host_id: str = BaseModule._DEFAULT_HOST_,
                         return_logs: bool = False):
        content = validate_message_content(prompt)
        content["logs"] = return_logs
        return self._make_request(method="POST",
                                  path=f"{self.root_path}/{host_id}/conversation/{conversation_id}/check_user_input",
                                  json_params=content)

    def check_model_output(self, conversation_id: str, prompt: str, host_id: str = BaseModule._DEFAULT_HOST_,
                           return_logs: bool = False):
        content = validate_message_content(prompt)
        content["logs"] = return_logs
        return self._make_request(method="POST",
                                  path=f"{self.root_path}/{host_id}/conversation/{conversation_id}/check_model_output",
                                  json_params=content)
