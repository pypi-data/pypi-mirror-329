from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from distutils.version import StrictVersion

from askoclics.askolib.dataset import DatasetClient
from askoclics.askolib.exceptions import AskoclicsAuthError, AskoclicsConnectionError, AskoclicsNotImplementedError
from askoclics.askolib.file import FileClient
from askoclics.askolib.result import ResultClient
from askoclics.askolib.sparql import SparqlClient

from future import standard_library

import requests

standard_library.install_aliases()


class AskomicsInstance(object):

    def __init__(self, api_key=None, url="http://localhost:80", proxy_username="", proxy_password="", **kwargs):

        if not api_key:
            raise AskoclicsAuthError("An api key is required")

        if proxy_username and proxy_password:
            self.auth = (proxy_username, proxy_password)
        else:
            self.auth = None

        self.api_key = api_key

        url = url.rstrip().rstrip("/")

        self.url = url

        self._check_connectivity()

        self.endpoints = self._get_endpoints()

        # Initialize Clients
        args = (self.url, self.endpoints, self.api_key, self.auth)
        self.file = FileClient(*args)
        self.dataset = DatasetClient(*args)
        self.result = ResultClient(*args)
        self.sparql = SparqlClient(*args)

    def __str__(self):
        return '<AskomicsInstance at {}>'.format(self.url)

    def _check_connectivity(self):
        headers = {"X-API-KEY": self.api_key}

        try:
            r = requests.get("{}/api/start".format(self.url), headers=headers, auth=self.auth)
            if not r.status_code == 200:
                raise requests.exceptions.RequestException

            data = r.json()

            if StrictVersion(data['config']['version']) < StrictVersion('4.3.0'):
                raise AskoclicsNotImplementedError("Askomics server version is older than 4.3.0.")

            if not data['config'].get("logged"):
                raise AskoclicsAuthError("Could not login with the provided API key.")

        except requests.exceptions.RequestException:
            raise AskoclicsConnectionError("Cannot connect to {}. Please check the connection.".format(self.url))

    def _get_endpoints(self):

        endpoints = {
            "start": "/api/start",
            "sparql_init": "/api/sparql/init",
            "sparql_preview": "/api/sparql/previewquery",
            "sparql_query": "/api/sparql/savequery",
            "upload_local_file": "/api/files/upload_chunk",
            "upload_url_file": "/api/files/upload_url",
            "list_files": "/api/files",
            "preview_files": "/api/files/preview",
            "delete_files": "/api/files/delete",
            "integrate_file": "/api/files/integrate",
            "list_datasets": "/api/datasets",
            "publicize_dataset": "/api/datasets/public",
            "delete_datasets": "/api/datasets/delete",
            "list_results": "/api/results",
            "preview_results": "/api/results/preview",
            "download_results": "/api/results/download",
            "delete_results": "/api/results/delete",
            "sparql_results": "/api/results/sparqlquery"
        }
        return endpoints


__version__ = '0.0.6'

PROJECT_NAME = "askoclics"
