from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os

from askoclics.askolib.client import Client

from future import standard_library


standard_library.install_aliases()


class SparqlClient(Client):
    """
    Send SPARQL queries to Askomics
    """

    def info(self):
        """
        Return available graphs, endpoints, and uris

        :rtype: dict
        :return: Dict with info
        """
        data = {}
        config = self._api_call("get", "start", {})
        data["namespace_data"] = config["config"]["namespaceData"]
        data["namespace_internal"] = config["config"]["namespaceInternal"]
        sparql_config = self._api_call("get", "sparql_init", {})
        data["graphs"] = sparql_config["graphs"]
        data["endpoints"] = sparql_config["endpoints"]
        return data

    def template(self, file_path):
        """
        Write the default query to a file

        :type file_path: str
        :param file_path: Path to the file to create

        :rtype: None
        :return: None
        """
        sparql_config = self._api_call("get", "sparql_init", {})
        with open(file_path, "w") as f:
            f.write(sparql_config["defaultQuery"])

    def query(self, query, graphs, endpoints, full_query=False):
        """
        Send a SPARQL query

        :type query: str
        :param query: Either a path to a file, or the query as a string

        :type graphs: str
        :param graphs: Comma-separated graphs

        :type endpoints: str
        :param endpoints: Comma-separated endpoints

        :type full_query: bool
        :param full_query: Whether to send a full query or a preview

        :rtype: dict
        :return: The API call result (either the result id, or the result preview)
        """
        data = {}

        if os.path.isfile(query):
            with open(query, 'r') as f:
                query = f.read()

        data["query"] = query
        data["graphs"] = self._parse_input_values(graphs, "Graphs")
        data["endpoints"] = self._parse_input_values(endpoints, "Endpoints")

        if full_query:
            return self._api_call("post", "sparql_query", data)
        else:
            return self._api_call("post", "sparql_preview", data)
