from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import json
import re

from askoclics.askolib.exceptions import AskoclicsApiError, AskoclicsConnectionError, AskoclicsNotImplementedError, AskoclicsParametersError

from future import standard_library

import requests

standard_library.install_aliases()


class Client(object):
    """
    Base client class implementing methods to make queries to the server
    """

    def __init__(self, url, endpoints, api_key, auth):
        self.url = url
        self.endpoints = endpoints
        self.api_key = api_key
        self.auth = auth

    def _api_call(self, call_type, endpoint_name, body={}, inline=False, download=False):

        headers = {"X-API-KEY": self.api_key}
        url = self._format_url(call_type, endpoint_name, body)

        try:
            if call_type == "get":
                if inline:
                    r = requests.get(url, params=body, headers=headers, auth=self.auth)
                else:
                    r = requests.get(url, headers=headers, auth=self.auth)
            elif call_type == "post":
                r = requests.post(url, json=body, headers=headers, auth=self.auth)

            if 400 <= r.status_code <= 499:
                mes = "API call returned a {} error".format(r.status_code)
                try:
                    res = r.json()
                    if res.get('errorMessage'):
                        mes += " : {}".format(res.get('errorMessage'))
                except json.decoder.JSONDecodeError:
                    pass
                raise AskoclicsApiError(mes)
            elif r.status_code == 502:
                raise AskoclicsApiError("Unknown server error")
            if download:
                return r.content
            res = r.json()
            if res.get('error'):
                raise AskoclicsApiError(res.get('errorMessage'))
            return res

        except requests.exceptions.RequestException:
            raise AskoclicsConnectionError("Cannot connect to {}. Please check the connection.".format(self.url))

    def _format_url(self, call_type, endpoint_name, body, inline=False):

        endpoint = self.endpoints.get(endpoint_name)
        if not endpoint:
            raise AskoclicsNotImplementedError()

        # Fill parameters in the url
        if not inline and call_type in ["get", "delete"]:
            groups = re.findall(r'<(.*?)>', endpoint)
            for group in groups:
                if group not in body:
                    raise AskoclicsApiError("Missing get parameter " + group)
                endpoint = endpoint.replace("<{}>".format(group), body.get(group))

        return "{}{}".format(self.url, endpoint)

    def _parse_input_values(self, val, val_name):

        if not val:
            return []

        if isinstance(val, list):
            return val
        elif isinstance(val, str):
            return [data.strip() for data in val.split(",")]
        else:
            raise AskoclicsParametersError("{} must either be a list or a comma-separated string".format(val_name))
