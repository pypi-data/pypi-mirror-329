from ..base_module import BaseModule


class Applications(BaseModule):
    root_path: str = "applications"

    def create(self, name: str, description: str, system_instructions: str, user_id: str, models: list[str] = None,
               datasets: list[str] = None) -> dict:
        """
        Create a new application.
        :param name: application name
        :param description: application description
        :param system_instructions: system instructions to be used by the application
        :param models: list of model ids
        :param datasets: list of dataset ids
        :param user_id: str user ID the new application will be related to
        :return: dictionary containing application creation response
        """
        return self._make_request(method="POST", path=f"{self.root_path}/",
                                  json_params={"name": name, "description": description,
                                               "system_instructions": system_instructions, "models": models,
                                               "datasets": datasets, "user_id": user_id})

    def delete(self, application_id: str) -> bool:
        """
        Delete an application by id
        :param application_id: str: application id to delete
        return True if delete succeeded, and False otherwise.
        """
        return self._make_request(method="DELETE", path=f"{self.root_path}/{application_id}")
