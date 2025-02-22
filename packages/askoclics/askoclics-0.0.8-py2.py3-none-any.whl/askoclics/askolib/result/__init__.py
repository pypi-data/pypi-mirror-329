from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os

from askoclics.askolib.client import Client
from askoclics.askolib.exceptions import AskoclicsParametersError

from future import standard_library


standard_library.install_aliases()


class ResultClient(Client):
    """
    Interact with AskOmics results
    """

    def list(self):
        """
        List results

        :rtype: dict
        :return: Dict with info
        """
        data = self._api_call("get", "list_results", {})
        data.pop('triplestoreMaxRows', None)
        return data

    def preview(self, result_id):
        """
        Show results preview

        :type result_id: str
        :param result_id: Result id

        :rtype: dict
        :return: Dict with info
        """
        return self._api_call("post", "preview_results", {"fileId": result_id})

    def download(self, result_id, file_path):
        """
        Download a result to a file

        :type result_id: str
        :param result_id: Result id

        :type file_path: str
        :param file_path: Output file path

        :rtype: None
        :return: None
        """

        if os.path.exists(file_path):
            raise AskoclicsParametersError("File {} already exists".format(file_path))
        data = self._api_call("post", "download_results", {"fileId": result_id}, download=True)
        with open(file_path, "w") as f:
            f.write(data)

    def delete(self, result_ids):
        """
        Delete results

        :type result_ids: str
        :param result_ids: Comma-separated result ids

        :rtype: None
        :return: None
        """
        data = {}
        data["filesIdToDelete"] = self._parse_input_values(result_ids, "Result ids")
        return self._api_call("post", "delete_results", data)

    def get_sparql(self, result_id):
        """
        Show results preview

        :type result_id: str
        :param result_id: Result id

        :rtype: dict
        :return: Dict with info
        """

        data = self._api_call("post", "sparql_results", {"fileId": result_id})
        data.pop("console_enabled", None)
        data.pop("disk_space", None)
        return data
