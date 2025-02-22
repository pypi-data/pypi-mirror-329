from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from askoclics.askolib.client import Client

from future import standard_library

standard_library.install_aliases()


class DatasetClient(Client):
    """
    Manipulate datasets managed by Askomics
    """

    def list(self):
        """
        List datasets added in Askomics

        :rtype: list
        :return: List of datasets
        """

        return self._api_call("get", "list_datasets", {})['datasets']

    def delete(self, datasets):
        """
        Send a delete task on a list of datasets

        :type datasets: str
        :param datasets: Comma-separated list of datasets IDs

        :rtype: list
        :return: List of the datasets
        """

        datasets = self._parse_input_values(datasets, "Datasets")
        body = {'datasetsIdToDelete': datasets}

        return self._api_call("post", "delete_datasets", body)

    def set_public(self, dataset_id):
        """
        Send a publicize task on a dataset

        :type datasets: str
        :param dataset: Id of the dataset to publish

        :rtype: list
        :return: List of the datasets
        """

        body = {
            'id': dataset_id,
            'newStatus': True
        }

        return self._api_call("post", "publicize_dataset", body)

    def set_private(self, dataset_id):
        """
        Send a privatize task on a dataset

        :type datasets: str
        :param dataset: Id of the dataset to privatize

        :rtype: list
        :return: List of the datasets
        """

        body = {
            'id': dataset_id,
            'newStatus': False
        }

        return self._api_call("post", "publicize_dataset", body)
