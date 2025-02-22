from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import mimetypes
import os

from askoclics.askolib.client import Client
from askoclics.askolib.exceptions import AskoclicsParametersError

from future import standard_library

import requests

standard_library.install_aliases()


class FileClient(Client):
    """
    Manipulate files managed by AskOmics
    """

    def list(self):
        """
        List files added in AskOmics

        :rtype: list
        :return: List with files
        """

        return self._api_call("get", "list_files", {})['files']

    def upload(self, url="", file_path="", verbose=False):
        """
        Upload a file to AskOmics

        :type url: str
        :param url: URL to the file

        :type file_path: str
        :param file_path: Path to the file to upload

        :type verbose: bool
        :param verbose: Show progression bar for local file upload

        :rtype: dict
        :return: Dict with results
        """
        if not (url or file_path) or (url and file_path):
            raise AskoclicsParametersError("Please provided either an url or a file path")

        if url:
            return self._api_call("post", "upload_url_file", {"url": url})

        if not os.path.isfile(file_path):
            raise AskoclicsParametersError("Local file not found")

        file_name = os.path.basename(file_path)
        internal_path = file_name
        mimetype = mimetypes.guess_type(file_path)[0]
        # Chunk size to 10 Mo
        file_size = os.stat(file_path).st_size
        chunk_size = 1024 * 1024 * 10
        first = True
        last = False
        uploaded_size = 0

        if file_size <= chunk_size:
            last = True

        with open(file_path, "rb") as f:
            if verbose:
                print("0%")

            for piece in self._read_in_chunks(f, chunk_size):
                if uploaded_size + chunk_size >= file_size:
                    last = True

                body = {"chunk": piece.decode("utf-8"), "first": first, "last": last, "type": mimetype, "name": file_name, "size": file_size, "path": internal_path}
                res = self._api_call("post", "upload_local_file", body)
                first = False
                internal_path = res["path"]
                uploaded_size += chunk_size
                if uploaded_size > file_size:
                    uploaded_size = file_size

                if verbose:
                    print("{0:.0%}".format(uploaded_size / file_size))

        return res

    def preview(self, files):
        """
        Get preview for a list of files

        :type files: str
        :param files: Comma-separated file IDs

        :rtype: dict
        :return: Dictionary containing the information
        """

        files = self._parse_input_values(files, "Files")
        body = {'filesId': files}

        return self._api_call("post", "preview_files", body)

    def describe(self, files):
        """
        Show file information

        :type files: str
        :param files: Comma-separated file IDs

        :rtype: list
        :return: List of files containing info
        """

        files = self._parse_input_values(files, "Files")
        body = {'filesId': files}

        res = self._api_call("post", "preview_files", body)

        files = []

        for file in res.get("previewFiles"):
            if "data" in file:
                file["data"].pop("content_preview", None)
            files.append(file)

        return files

    def integrate_csv(self, file_id, columns="", headers="", force=False, custom_uri=None, skip_preview=False, public=False):
        """
        Send an integration task for a specified file_id

        :type file_id: str
        :param file_id: File_id

        :type columns: str
        :param columns: Comma-separated columns (default to detected columns)

        :type headers: str
        :param headers: Comma-separated headers (default to file headers)

        :type force: bool
        :param force: Ignore the content type mismatch (ex: force an integer type when AskOmics detects a text type)

        :type custom_uri: str
        :param custom_uri: Custom uri

        :type skip_preview: bool
        :param skip_preview: Skip the preview step for big files

        :type public: bool
        :param public: Set the file as public (admin only)

        :rtype: dict
        :return: Dictionary of task information
        """

        columns = self._parse_input_values(columns, "Columns")
        headers = self._parse_input_values(headers, "Headers")

        if not skip_preview:

            data = self._check_integrate_file(file_id, "csv/tsv")

            if headers and not len(headers) == len(data["header"]):
                raise AskoclicsParametersError("Incorrect number of headers : {} headers supplied, {} headers expected".format(len(headers), len(data["header"])))

            if columns:
                if not len(columns) == len(data["columns_type"]):
                    raise AskoclicsParametersError("Incorrect number of columns : {} columns supplied, {} columns expected".format(len(columns), len(data["columns_type"])))

                expected_columns = self._get_column_types()
                for index, val in enumerate(columns):
                    if index == 0:
                        if val not in ["start_entity", "entity"]:
                            raise AskoclicsParametersError("First column type must be either start_entity or entity")
                        continue

                    if val not in expected_columns:
                        raise AskoclicsParametersError("Column type {} is not supported by AskOmics. Supported column types are {}".format(val, expected_columns))

                if not force:
                    for index, value in enumerate(data["columns_type"]):
                        if value == "text" and columns[index] not in ["text", "category", "general_relation", "symetric_relation"]:
                            raise AskoclicsParametersError("Type mismatch on provided column {} : provided type is {}, but AskOmics predicted {}. To proceed, use the force parameter".format(index + 1, columns[index], value))

        body = {"fileId": file_id, "columns_type": columns, "header_names": headers, "customUri": custom_uri, "public": public}
        return self._api_call("post", "integrate_file", body)

    def integrate_bed(self, file_id, entity="", custom_uri=None, skip_preview=False, public=False):
        """
        Send an integration task for a specified file_id

        :type file_id: str
        :param file_id: File_id

        :type entity: str
        :param entity: Name of the entity (default to file name)

        :type custom_uri: str
        :param custom_uri: Custom uri

        :type skip_preview: bool
        :param skip_preview: Skip the preview step for big files

        :type public: bool
        :param public: Set the file as public (admin only)

        :rtype: dict
        :return: Dictionary of task information
        """

        if not skip_preview:
            self._check_integrate_file(file_id, "bed")

        body = {"fileId": file_id, "entity_name": entity, "customUri": custom_uri, "public": public}
        return self._api_call("post", "integrate_file", body)

    def integrate_gff(self, file_id, entities="", custom_uri=None, skip_preview=False, public=False):
        """
        Send an integration task for a specified file_id

        :type file_id: str
        :param file_id: File_id

        :type entities: str
        :param entities: Comma-separated list of entities to integrate. (Default to all available entities)

        :type custom_uri: str
        :param custom_uri: Custom uri

        :type skip_preview: bool
        :param skip_preview: Skip the preview step for big files

        :type public: bool
        :param public: Set the file as public (admin only)

        :rtype: dict
        :return: Dictionary of task information
        """

        entities = self._parse_input_values(entities, "Entities")

        if not skip_preview:
            data = self._check_integrate_file(file_id, "gff/gff3")
            if entities:
                for entity in entities:
                    if entity not in data['entities']:
                        AskoclicsParametersError("Entity {} was not detected in the file. Detected entities are : {} ".format(entity, data['entities']))

        body = {"fileId": file_id, "entities": entities, "customUri": custom_uri, "public": public}
        return self._api_call("post", "integrate_file", body)

    def integrate_rdf(self, file_id, external_endpoint=None, skip_preview=False, public=False):
        """
        Send an integration task for a specified file_id

        :type file_id: str
        :param file_id: File_id

        :type external_endpoint: str
        :param external_endpoint: External endpoint

        :type skip_preview: bool
        :param skip_preview: Skip the preview step for big files

        :type public: bool
        :param public: Set the file as public (admin only)

        :rtype: dict
        :return: Dictionary of task information

        """

        if not skip_preview:
            self._check_integrate_file(file_id, "rdf/ttl")

        body = {"fileId": file_id, "externalEndpoint": external_endpoint, "public": public}
        return self._api_call("post", "integrate_file", body)

    def delete(self, files):
        """
        Delete a list of files

        :type files: str
        :param files: Comma-separated file IDs to delete

        :rtype: dict
        :return: Dictionary containing the remaining files
        """

        files = self._parse_input_values(files, "Files")
        body = {'filesIdToDelete': files}

        return self._api_call("post", "delete_files", body)

    def _read_in_chunks(self, file_object, chunk_size):
        """Lazy function (generator) to read a file piece by piece.
        Default chunk size: 10 Mo."""
        while True:
            data = file_object.read(chunk_size)
            if not data:
                break
            yield data

    def _check_integrate_file(self, file_id, file_type):
        # Check if file exists
        # Then check if type is correct
        # Return predicted columns/types if csv/bed

        body = {'filesId': [file_id]}
        res = self._api_call("post", "preview_files", body)

        files = res.get("previewFiles")

        if not files:
            raise AskoclicsParametersError("File with id {} not found".format(file_id))

        file = files[0]

        if file["error"]:
            raise AskoclicsParametersError("File is in error state : {}".format(file["error_message"]))

        if not file["type"] == file_type:
            raise AskoclicsParametersError("Incorrect file type : Selected type is {}, selected file type is {}".format(file_type, file["type"]))

        return file.get("data")

    def _get_column_types(self):
        r = requests.get("{}/api/files/columns".format(self.url), auth=self.auth)
        if not r.status_code == 200:
            raise requests.exceptions.RequestException

        data = r.json()
        return data["types"]
