import os
import sys
import time
from typing import List, Union
from urllib.parse import parse_qs, urlparse

from pydantic import BaseModel  # pylint: disable=no-name-in-module

from . import _constants as constants
from ._utils import RequestMode, parse_to_str, request

class Connector:
    def __init__(
        self,
        domain: str,
        token: str,
        verify_ssl: bool = False,
    ):
        self._token = token
        self._verify_ssl = verify_ssl

        link = urlparse(domain)
        if len(link.netloc) == 0:
            raise Exception("invalid domain: {}".format(domain))

        params = dict(parse_qs(link.query))
        params = {k: v[0] for k, v in params.items()}
        self.params = params
        self._domain = "{}://{}{}".format(link.scheme, link.netloc, link.path)

    def request(
            self,
            url: str,
            params: dict = {},
            json: dict = {},
            data: dict = {},
            mode: str = RequestMode.POST,
            files: dict = {},
    ):
        for k, v in self.params.items():
            params[k] = v

        res = request(
            url=url.replace(os.sep, "/"),
            params=params,
            json=json,
            data=data,
            files=files,
            headers={constants.TOKEN_KEY: self._token},
            mode=mode,
            verify=self._verify_ssl
        )
        if res[constants.ConnectorKeys.STATUS] != 0:
            raise Exception(parse_to_str(res))

        return res[constants.ConnectorKeys.MESSAGE]

    def post_openapi_request(
            self, url: str,
            params: dict = {},
            json: dict = {},
            data: dict = {},
            mode: str = RequestMode.POST,
            files: dict = {},
    ) -> dict:
        return self.request(
            os.path.join(self._domain, constants.OPEN_API, url),
            params=params, json=json, data=data,
            mode=mode, files=files,
        )


class OpenAPI(Connector):
    @property
    def info(self):
        return self.post_openapi_request(
            url=constants.INFO_URL,
            mode=RequestMode.GET,
        )

    @property
    def mounts(self):
        return self.post_openapi_request(
            url=constants.EXTERNAL_MOUNT_URL,
            mode=RequestMode.GET,
        )

    @property
    def groups(self):
        return self.post_openapi_request(
            url=constants.GROUPS_URL,
            mode=RequestMode.GET,
        )

    @property
    def get_user_s3(self):
        return self.post_openapi_request(
            url=constants.LIST_S3,
            mode=RequestMode.POST,
        )
    
    def list_projects(self, json: dict = {}):
        return self.post_openapi_request(
            url=constants.PROJECTS_URL,
            json=json,
            mode=RequestMode.POST,
        )

    def list_dir(self, path: str, ignore_hidden: bool = True):
        return self.post_openapi_request(
            constants.LIST_URL,
            data={
                constants.ConnectorKeys.PATH: path,
                constants.ConnectorKeys.IGNORE_HIDDEN: ignore_hidden,
            }
        )

    def create_project(
        self,
        group_id: str,
        species: str,
        project_name: str,
        matrix_paths: list[str],
        metadata_paths: list[str],
        dataset_name: str = 'Dataset TBD',
        project_id: str = '',
        use_gene_symbols: bool = True,
        platform: int = 0,
        sdk_version: str = '',
    ):
        return self.post_openapi_request(
            url=constants.CREATE_PROJECT_URL,
            json={
                constants.ConnectorKeys.BG_MODE: 1,
                constants.ConnectorKeys.PROJECT_NAME: project_name,
                constants.ConnectorKeys.MATRIX_PATH_LIST: ",".join(matrix_paths),
                constants.ConnectorKeys.MATRIX_SHEET_LIST: ",".join(["-1" for _ in range(len(matrix_paths))]),
                constants.ConnectorKeys.METADATA_PATH_LIST: ",".join(metadata_paths),
                constants.ConnectorKeys.METADATA_SHEET_LIST: ",".join(["-1" for _ in range(len(metadata_paths))]),
                constants.ConnectorKeys.INIT_OPTION: 'merge_intersect',
                constants.ConnectorKeys.INIT_PROJECT_UUID: project_id,
                constants.ConnectorKeys.DATASET_NAME_LIST: ",".join(
                    [dataset_name for _ in range(len(metadata_paths))]),
                constants.ConnectorKeys.GROUP_ID: group_id,
                constants.ConnectorKeys.SPECIES: species,
                constants.ConnectorKeys.USE_GENE_SYMBOLS: int(use_gene_symbols),
                constants.ConnectorKeys.PLATFORM: platform,
                constants.ConnectorKeys.SDK_VERSION: sdk_version,
            }
        )
    
    def create_nanostring_project(
        self,
        group_id: str,
        species: str,
        project_name: str,
        rcc_folder_path: str,
        matrix_path: str = '',
        metadata_path: str = '',
        dataset_name: str = 'Dataset TBD',
        project_id: str = '',
        aggregate_count: bool = False,
        platform: int = 1,
        sdk_version: str = '',
    ):
        return self.post_openapi_request(
            url=constants.CREATE_NANOSTRING_PROJECT_URL,
            json={
                constants.ConnectorKeys.BG_MODE: 1,
                constants.ConnectorKeys.PROJECT_NAME: project_name,
                constants.ConnectorKeys.RCC_FOLDER_PATH: rcc_folder_path,
                constants.ConnectorKeys.MATRIX_PATH_LIST: matrix_path,
                constants.ConnectorKeys.MATRIX_SHEET_LIST: '-1',
                constants.ConnectorKeys.METADATA_PATH_LIST: metadata_path,
                constants.ConnectorKeys.METADATA_SHEET_LIST: '-1',
                constants.ConnectorKeys.INIT_PROJECT_UUID: project_id,
                constants.ConnectorKeys.DATASET_NAME_LIST: dataset_name,
                constants.ConnectorKeys.GROUP_ID: group_id,
                constants.ConnectorKeys.SPECIES: species,
                constants.ConnectorKeys.AGGREGATE_COUNT: int(aggregate_count),
                constants.ConnectorKeys.PLATFORM: platform,
                constants.ConnectorKeys.SDK_VERSION: sdk_version,
            }
        )

    def get_file_content(self, path: str):
        return self.post_openapi_request(
            url=constants.GET_FILE_CONTENT_URL,
            json={
                constants.ConnectorKeys.FILE: path,

            },
        )
    
    def check_file_exists(self, path: str):
        return self.post_openapi_request(
            url=constants.CHECK_FILE_EXISTS_URL,
            json={
                constants.ConnectorKeys.FILE: path,

            },
        )

    def upload_file(
        self, file_path: str,
        folder_name: str, upload_id: str,
        is_chunk: bool,
    ):
        file = open(file_path, "rb")
        resp = self.post_openapi_request(
            url=constants.UPLOAD_FILE_URL,
            data={
                constants.ConnectorKeys.UPLOAD_FOLDER_NAME: folder_name,
                constants.ConnectorKeys.UPLOAD_UNIQUE_ID: upload_id,
                constants.ConnectorKeys.UPLOAD_IS_CHUNK: is_chunk,
            },
            files={
                constants.ConnectorKeys.UPLOAD_FILE_DATA: file,
            },
        )
        file.close()
        return resp

    def upload_chunk_start(self, folder_name: str, parent_is_file: int):
        return self.post_openapi_request(
            url=constants.UPLOAD_CHUNK_START_URL,
            json={
                constants.ConnectorKeys.UPLOAD_FOLDER_NAME: folder_name,
                constants.ConnectorKeys.UPLOAD_PARENT_IS_FILE: parent_is_file,
            }
        )

    def upload_chunk_process(
        self,
        chunk_size: int,
        file_size: int,
        offset: int,
        file_name: str,
        folder_name: str,
        upload_id: str,
        path: str,
        sending_index: int,
        parent_is_file: int,
        file_data: list[str],
    ):
        return self.post_openapi_request(
            url=constants.UPLOAD_CHUNK_PROCESS_URL,
            data={
                constants.ConnectorKeys.UPLOAD_FOLDER_NAME: folder_name,
                constants.ConnectorKeys.UPLOAD_PARENT_IS_FILE: parent_is_file,
                constants.ConnectorKeys.UPLOAD_CHUNK_SIZE: chunk_size,
                constants.ConnectorKeys.UPLOAD_FILE_SIZE: file_size,
                constants.ConnectorKeys.UPLOAD_OFFSET: offset,
                constants.ConnectorKeys.UPLOAD_FILE_NAME: file_name,
                constants.ConnectorKeys.UPLOAD_UNIQUE_ID: upload_id,
                constants.ConnectorKeys.UPLOAD_PATH: path,
                constants.ConnectorKeys.UPLOAD_SENDING_INDEX: sending_index,
            },
            files={
                constants.ConnectorKeys.UPLOAD_FILE_DATA: file_data,
            }
        )

    def upload_chunk_merge(
        self,
        total_chunk: int,
        file_name: str,
        folder_name: str,
        upload_id: str,
        path: str,
        parent_is_file: int,
        move_to_parent: bool,
    ):
        return self.post_openapi_request(
            url=constants.UPLOAD_CHUNK_MERGE_URL,
            json={
                constants.ConnectorKeys.UPLOAD_FOLDER_NAME: folder_name,
                constants.ConnectorKeys.UPLOAD_PARENT_IS_FILE: parent_is_file,
                constants.ConnectorKeys.UPLOAD_TOTAL_CHUNK: total_chunk,
                constants.ConnectorKeys.UPLOAD_FILE_NAME: file_name,
                constants.ConnectorKeys.UPLOAD_UNIQUE_ID: upload_id,
                constants.ConnectorKeys.UPLOAD_PATH: path,
                constants.ConnectorKeys.UPLOAD_MOVE_TO_PARENT: move_to_parent,
            }
        )

    def upload_folder_finish(self, folder_name: str, upload_id: str):
        return self.post_openapi_request(
            url=constants.UPLOAD_FOLDER_FINISH_URL,
            data={
                constants.ConnectorKeys.UPLOAD_FOLDER_NAME: folder_name,
                constants.ConnectorKeys.UPLOAD_UNIQUE_ID: upload_id,
            },
        )
