from typing import Union, List, Dict
import os
from urllib.parse import urlparse, parse_qs

from pydantic import BaseModel  # pylint: disable=no-name-in-module

from . import _constants as constants
from ._utils import RequestMode
from ._utils import request
from ._utils import parse_to_str


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
        if res[constants.ConnectorKeys.STATUS.value] != 0:
            raise Exception(parse_to_str(res))

        return res[constants.ConnectorKeys.MESSAGE.value]

    def post_pyapi_request(
            self, url: str,
            params: dict = {},
            json: dict = {},
            data: dict = {},
            mode: str = RequestMode.POST,
            files: dict = {},
    ) -> Union[BaseModel, str]:
        return self.request(
            os.path.join(self._domain, constants.V1_API, url),
            params=params, json=json, data=data,
            mode=mode, files=files,
        )

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


class PyAPI(Connector):
    def parse_data_information(self, name: str, technology: str, data_path: str) -> dict:
        return self.post_pyapi_request(
            url=constants.PARSE_DATA_URL,
            json={
                constants.ConnectorKeys.DATA_NAME.value: name,
                constants.ConnectorKeys.TECHNOLOGY.value: technology,
                constants.ConnectorKeys.DATA_PATH.value: data_path,
            }
        )

    def get_sample_info(
        self,
        study_path: str,
        sample_id: str,
    ):
        return self.post_pyapi_request(
            url=constants.SAMPLE_INFO_URL,
            json={
                constants.ConnectorKeys.STUDY_PATH.value: study_path,
                constants.ConnectorKeys.SAMPLE_ID.value: sample_id,
            },
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

    def list_s3(self, offset: int = 0, limit: int = 100):
        return self.post_openapi_request(
            url=constants.LIST_S3,
            mode=RequestMode.POST,
            data={
                constants.ConnectorKeys.LIMIT.value: limit,
                constants.ConnectorKeys.OFFSET.value: offset,
            }
        )

    @property
    def s3(self):
        return self.list_s3()

    @property
    def groups(self):
        return self.post_openapi_request(
            url=constants.GROUPS_URL,
            mode=RequestMode.GET,
        )

    def list_dir(self, path: str, ignore_hidden: bool = True):
        return self.post_openapi_request(
            constants.LIST_URL,
            data={
                constants.ConnectorKeys.PATH.value: path,
                constants.ConnectorKeys.IGNORE_HIDDEN.value: ignore_hidden,
            }
        )

    def create_study(
        self,
        group_id: str,
        species: str,
        title: str,
        create_type: int = constants.StudyType.SPATIAL_STUDY_TYPE_NUMBER.value,
    ):
        return self.post_openapi_request(
            url=constants.CREATE_STUDY_URL,
            json={
                constants.ConnectorKeys.GROUP_ID.value: group_id,
                constants.ConnectorKeys.SPECIES.value: species,
                constants.ConnectorKeys.TITLE.value: title,
                constants.ConnectorKeys.TYPE.value: create_type,
            }
        )

    def list_study(
        self,
        group_id: str,
        species: str,
        limit: int = 50,
        offset: int = 0,
        active: int = constants.StudyStatus.PROCESSING_STATUS.value,
        compare: int = constants.StudyFilter.NOT_LARGER.value,
    ):
        return self.post_openapi_request(
            url=constants.LIST_STUDY_URL,
            data={
                constants.ConnectorKeys.GROUP_ID.value: group_id,
                constants.ConnectorKeys.SPECIES.value: species,
                constants.ConnectorKeys.LIMIT.value: limit,
                constants.ConnectorKeys.OFFSET.value: offset,
                constants.ConnectorKeys.ACTIVE.value: active,
                constants.ConnectorKeys.COMPARE.value: compare,
            }
        )

    def get_study_detail(self, study_id: str, limit: int = 50, offset: int = 0):
        return self.post_openapi_request(
            url=constants.DETAIL_STUDY_URL,
            params={
                constants.ConnectorKeys.KEY.value: study_id,
                constants.ConnectorKeys.LIMIT.value: limit,
                constants.ConnectorKeys.OFFSET.value: offset,
            },
            mode=RequestMode.GET,
        )

    def create_sample(
        self,
        study_id: str,
        name: str,
        data: List[dict],
    ):
        return self.post_openapi_request(
            url=constants.CREATE_SAMPLE_URL,
            json={
                constants.ConnectorKeys.STUDY_ID.value: study_id,
                constants.ConnectorKeys.NAME.value: name,
                constants.ConnectorKeys.DATA.value: data,
            }
        )

    def add_sample_data(
        self,
        study_id: str,
        sample_id: str,
        data: List[dict],
    ):
        return self.post_openapi_request(
            url=constants.ADD_SAMPLE_DATA_URL,
            json={
                constants.ConnectorKeys.STUDY_ID.value: study_id,
                constants.ConnectorKeys.SAMPLE_ID.value: sample_id,
                constants.ConnectorKeys.DATA.value: data,
            }
        )

    def add_sample_data_element(
        self,
        title: str,
        study_id: str,
        sample_id: str,
        data_id: str,
        identities: List[str] = [],
        files: List[Dict[str, str]] = [],
        folders: List[Dict[str, str]] = [],
        args: List[Dict[str, str]] = [],
    ):
        return self.post_openapi_request(
            url=constants.ADD_URL,
            json={
                constants.ConnectorKeys.TITLE.value: title,
                constants.ConnectorKeys.STUDY_ID.value: study_id,
                constants.ConnectorKeys.SAMPLE_ID.value: sample_id,
                constants.ConnectorKeys.DATA_ID.value: data_id,
                constants.ConnectorKeys.FILES.value: files,
                constants.ConnectorKeys.FOLDERS.value: folders,
                constants.ConnectorKeys.ARGS.value: args,
                constants.ConnectorKeys.IDENTITIES.value: identities,
            },
        )

    def list_sample(
        self,
        study_id: str,
        limit: int = 50,
        offset: int = 0,
        need_data: bool = False,
    ):
        return self.post_openapi_request(
            url=constants.LIST_SAMPLE_URL,
            params={
                constants.ConnectorKeys.KEY.value: study_id,
                constants.ConnectorKeys.LIMIT.value: limit,
                constants.ConnectorKeys.OFFSET.value: offset,
                constants.ConnectorKeys.NEED_DATA.value: need_data,
            },
            mode=RequestMode.GET,
        )

    def get_sample_detail(self, sample_id: str, limit: int = 50, offset: int = 0):
        return self.post_openapi_request(
            url=constants.DETAIL_SAMPLE_URL,
            params={
                constants.ConnectorKeys.KEY.value: sample_id,
                constants.ConnectorKeys.LIMIT.value: limit,
                constants.ConnectorKeys.OFFSET.value: offset,
            },
            mode=RequestMode.GET,
        )

    def get_sample_data_detail(self, data_id: str, limit: int = 50, offset: int = 0):
        return self.post_openapi_request(
            url=constants.DETAIL_SAMPLE_DATA_URL,
            params={
                constants.ConnectorKeys.KEY.value: data_id,
                constants.ConnectorKeys.LIMIT.value: limit,
                constants.ConnectorKeys.OFFSET.value: offset,
            },
            mode=RequestMode.GET,
        )

    def list_public_study(
        self,
        group_id: str,
        species: str,
        limit: int = 50,
        offset: int = 0,
        active: int = constants.StudyStatus.PROCESSING_STATUS.value,
    ):
        return self.post_openapi_request(
            url=constants.LIST_PUBLIC_STUDY_URL,
            json={
                constants.ConnectorKeys.GROUP_ID.value: group_id,
                constants.ConnectorKeys.SPECIES.value: species,
                constants.ConnectorKeys.LIMIT.value: limit,
                constants.ConnectorKeys.OFFSET.value: offset,
                constants.ConnectorKeys.ACTIVE.value: active,
            }
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
                constants.ConnectorKeys.UPLOAD_FOLDER_NAME.value: folder_name,
                constants.ConnectorKeys.UPLOAD_UNIQUE_ID.value: upload_id,
                constants.ConnectorKeys.UPLOAD_IS_CHUNK.value: is_chunk,
            },
            files={
                constants.ConnectorKeys.UPLOAD_FILE_DATA.value: file,
            },
        )
        file.close()
        return resp

    def upload_chunk_start(self, folder_name: str, parent_is_file: int):
        return self.post_openapi_request(
            url=constants.UPLOAD_CHUNK_START_URL,
            json={
                constants.ConnectorKeys.UPLOAD_FOLDER_NAME.value: folder_name,
                constants.ConnectorKeys.UPLOAD_PARENT_IS_FILE.value: parent_is_file,
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
                constants.ConnectorKeys.UPLOAD_FOLDER_NAME.value: folder_name,
                constants.ConnectorKeys.UPLOAD_PARENT_IS_FILE.value: parent_is_file,
                constants.ConnectorKeys.UPLOAD_CHUNK_SIZE.value: chunk_size,
                constants.ConnectorKeys.UPLOAD_FILE_SIZE.value: file_size,
                constants.ConnectorKeys.UPLOAD_OFFSET.value: offset,
                constants.ConnectorKeys.UPLOAD_FILE_NAME.value: file_name,
                constants.ConnectorKeys.UPLOAD_UNIQUE_ID.value: upload_id,
                constants.ConnectorKeys.UPLOAD_PATH.value: path,
                constants.ConnectorKeys.UPLOAD_SENDING_INDEX.value: sending_index,
            },
            files={
                constants.ConnectorKeys.UPLOAD_FILE_DATA.value: file_data,
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
                constants.ConnectorKeys.UPLOAD_FOLDER_NAME.value: folder_name,
                constants.ConnectorKeys.UPLOAD_PARENT_IS_FILE.value: parent_is_file,
                constants.ConnectorKeys.UPLOAD_TOTAL_CHUNK.value: total_chunk,
                constants.ConnectorKeys.UPLOAD_FILE_NAME.value: file_name,
                constants.ConnectorKeys.UPLOAD_UNIQUE_ID.value: upload_id,
                constants.ConnectorKeys.UPLOAD_PATH.value: path,
                constants.ConnectorKeys.UPLOAD_MOVE_TO_PARENT.value: move_to_parent,
            }
        )

    def upload_folder_finish(self, folder_name: str, upload_id: str):
        return self.post_openapi_request(
            url=constants.UPLOAD_FOLDER_FINISH_URL,
            data={
                constants.ConnectorKeys.UPLOAD_FOLDER_NAME.value: folder_name,
                constants.ConnectorKeys.UPLOAD_UNIQUE_ID.value: upload_id,
            },
        )

    def convert_from_lens(
        self, study_id: str, study_name: str,
        group_id: str, species: str, lens_data_path: str
    ):
        return self.post_openapi_request(
            url=constants.STUDY_CONVERT_FROM_LENS_URL,
            data={
                constants.ConnectorKeys.STUDY_ID.value: study_id,
                constants.ConnectorKeys.TITLE.value: study_name,
                constants.ConnectorKeys.GROUP_ID.value: group_id,
                constants.ConnectorKeys.SPECIES.value: species,
                constants.ConnectorKeys.LENS_DATA_PATH.value: lens_data_path,
            }
        )
