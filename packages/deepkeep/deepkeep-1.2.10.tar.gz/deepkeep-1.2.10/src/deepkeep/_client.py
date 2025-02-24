import os
import requests
import importlib
import pkgutil
from functools import cached_property
from typing import Union

from deepkeep._exceptions import DeepkeepError
from deepkeep.modules.base_module import BaseModule


class Deepkeep:
    """
    Class that represents the DeepKeep.ai Client
    """
    # client options
    _access_key: str
    _secret_key: str
    _organization: Union[str, None]

    _request_helpers: dict = {}

    def __init__(self, access_key: Union[str, None] = None, secret_key: Union[str, None] = None,
                 organization: Union[str, None] = None, base_url: Union[str, None] = None,
                 timeout: Union[int, None] = None, max_retries: int = 0, token: str = None, **kwargs):
        """Construct a new synchronous deepkeep client instance.

        This automatically infers the following arguments from their corresponding environment variables if they are not provided:
        - `access_key` from `DEEPKEEP_ACCESS_KEY`
        - `secret_key` from `DEEPKEEP_SECRET_KEY`
        - `organization` from `DEEPKEEP_ORG_ID`
        """
        self._token = token

        # In case token is not provided, access_key and secret_key are mandatory
        # enforcing access key and setting it
        if access_key is None:
            access_key = os.environ.get("DEEPKEEP_ACCESS_KEY")
        if token is None and access_key is None:
            raise DeepkeepError("The access_key client option must be set either by passing access_key to the client "
                                "or by setting the DEEPKEEP_ACCESS_KEY environment variable")
        self.access_key = access_key

        # enforcing access key and setting it
        if secret_key is None:
            secret_key = os.environ.get("DEEPKEEP_SECRET_KEY")
        if token is None and secret_key is None:
            raise DeepkeepError("The secret_key client option must be set either by passing secret_key to the client "
                                "or by setting the DEEPKEEP_SECRET_KEY environment variable")
        self.secret_key = secret_key

        # setting organization
        if organization is None:
            organization = os.environ.get("DEEPKEEP_ORG_ID")
        self.organization = organization

        # setting base url
        if base_url is None:
            base_url = os.environ.get("DEEPKEEP_BASE_URL")
        if base_url is None:
            base_url = f"https://api.deepkeep.com/api/latest"
        self.base_url = base_url

        # headers
        self.request_helpers: dict = {}

        # loading modules
        self._load_modules()

    @property
    def access_key(self) -> str:
        return self._access_key

    @access_key.setter
    def access_key(self, value: str):
        self._access_key = value

    @property
    def secret_key(self) -> str:
        return self._secret_key

    @secret_key.setter
    def secret_key(self, value: str):
        self._secret_key = value

    @property
    def organization(self) -> Union[str, None]:
        return self._organization

    @organization.setter
    def organization(self, value: Union[str, None]):
        self._organization = value

    @cached_property
    def token(self) -> Union[str, None]:
        # connect to API
        if not self._token:
            self._connect()

        return self._token

    @cached_property
    def auth_headers(self) -> dict[str, str]:
        return {"Authorization": f"Bearer {self.token}"}

    def _load_modules(self):
        # Assuming "modules" is the directory where your module classes are defined
        package = 'deepkeep.modules'
        package_obj = importlib.import_module(package)

        for _, module_name, _ in pkgutil.iter_modules(package_obj.__path__):
            module = importlib.import_module(f"{package}.{module_name}")
            for attribute_name in dir(module):
                attribute = getattr(module, attribute_name)
                if isinstance(attribute, type) and issubclass(attribute, BaseModule) and attribute is not BaseModule:
                    self._add_property(attribute_name.lower(), attribute)

    def _add_property(self, name, cls):
        def getter(self):
            return cls(self)
        setattr(Deepkeep, name, property(getter))

    def _connect(self):
        """

        :return:
        """
        # get API token
        _api_res = requests.post(f"{self.base_url}/auth/", data={
            "username": self.access_key,
            "password": self.secret_key
        })

        # check authorization
        if not _api_res.ok:
            raise DeepkeepError(f"failed authorization for user {self.access_key}")

        # sett API token
        self._token = _api_res.json().get("access_token")

Client = Deepkeep
