from dataclasses import dataclass
from typing import Union
from time import sleep

from deepkeep._exceptions import DeepkeepError
from ..base_module import BaseModule, BaseData

__all__ = ["Message"]


@dataclass
class MessageData(BaseData):
    content: str

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


def validate_message_content(content: Union[MessageData, dict, str, None] = None) -> dict:
    """
    Validates and converts the input content to a dictionary format.

    Args:
        content (MessageData | dict | str | None, optional):
            The input content to be validated. It can be:
            - `MessageData`: an instance of `MessageData`.
            - `dict`: a dictionary to initialize a `MessageData` instance.
            - `str`: a string representing the message content.
            - `None`: if no content is provided, a default `MessageData` instance will be created.

    Returns:
        dict: A dictionary representation of the validated `MessageData` instance.

    Raises:
        DeepkeepError: If the input content is not of type `MessageData`, `dict`, or `str`.
    """
    content = content or MessageData()

    if isinstance(content, dict):
        content = MessageData(**content)
    elif isinstance(content, str):
        content = MessageData(content=content)
    elif not isinstance(content, MessageData):
        raise DeepkeepError("input content is not valid. should be one of the following type: "
                            "\n\tdeepkeep.modules.Message | dict | str")
    return content.as_dict()


class Message(BaseModule):
    root_path: str = "monitoring"

    def create(self, conversation_id: str, host_id: str = BaseModule._DEFAULT_HOST_,
               content: Union[MessageData, dict, str, None] = None, user_id: Union[str, None] = None,
               verbose: bool = False, return_logs: bool = False):
        additional_details = {}
        dict_content = validate_message_content(content)
        dict_content["logs"] = return_logs

        if user_id and isinstance(user_id, str):
            additional_details = {
                "headers": {
                    "user": user_id
                }
            }

        _res = self._make_request(method="POST", path=f"{self.root_path}/{host_id}/chat/{conversation_id}/message",
                                  json_params=dict_content, **additional_details)

        if _res and verbose:
            request_id = _res.get("request_id")

            # TODO: fix and beautify retry
            # get extra data
            for _retry in range(5):
                try:
                    sleep(0.5)
                    _res_verbose = self._make_request(path=f"report/statistics/message/{request_id}",
                                                      **additional_details)

                    _res |= {"statistics": _res_verbose}
                    break
                except DeepkeepError as verbose_error:
                    _res |= {"statistics": {"error": verbose_error}}

        return _res

    def get(self, conversation_id: str, host_id: str = BaseModule._DEFAULT_HOST_):
        return self._make_request(path=f"{self.root_path}/{host_id}/chat/{conversation_id}/messages")

    def statistics(self, request_id: str):
        return self._make_request(path=f"report/statistics/message/{request_id}")
