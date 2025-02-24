from typing import List, Dict, Union, Optional
import os
from tqdm import tqdm
from pathlib import Path

from ._api import Connector
from ._api import PyAPI
from ._api import OpenAPI
from ._analysis import Analysis
from ._constants import ConnectorKeys
from ._constants import DefaultGroup
from ._utils import get_chunk_size, format_print


class SpatialXConnector(Connector):
    """
    SpatialX Connector
    Supporting to work with spatial data via notebook.
    """

    def __init__(self, domain: str, token: str, verify_ssl: bool = False):
        """
        Construct parameters for train and query k-nearest neighbors

        Parameters
        ----------
        domain: ``str``
            SpatialX domain
        token: ``str``
            User's token
        verify_ssl: ``bool``, default: False
            Verify SSL or not.
        """
        super().__init__(domain, token, verify_ssl)

        self.__pyapi = PyAPI(domain, token, verify_ssl)
        self.__openapi = OpenAPI(domain, token, verify_ssl)
        self.__analysis = Analysis(domain, token, verify_ssl)

    @property
    def pyapi(self) -> PyAPI:
        return self.__pyapi

    @property
    def openapi(self) -> OpenAPI:
        return self.__openapi

    @property
    def analysis(self) -> Analysis:
        return self.__analysis

    @property
    def info(self):
        """Current user's information"""
        info = self.openapi.info
        return {
            field: info[field]
            for field in ConnectorKeys.INFORMATION_FIELDS.value
        }

    @property
    def groups(self):
        """List all reachable groups of current user in domain server."""
        group_info = self.openapi.groups
        groups = {
            v: k for k, v in group_info[ConnectorKeys.DEFAULT.value].items()
        }
        for group in group_info[ConnectorKeys.GROUPS.value]:
            groups[group["name"]] = group["id"]
        return groups

    @property
    def external_folders(self):
        """List all reachable mounted shared folders of current user from BBrowserX/BioStudio."""
        return {
            folder["name"]: folder["path"]
            for folder in self.openapi.mounts["folders"]
        }

    @property
    def folders(self):
        """List all reachable mounted shared folders of current user in domain server."""
        defaults = {
            folder["name"]: folder["path"]
            for folder in self.openapi.info["default_mount"]["folders"]
        }
        return dict(self.external_folders.items() | defaults.items())

    @property
    def s3(self):
        """List all reachable mounted s3 clouds of current user in domain server."""
        s3_buckets = {}
        for s3 in self.openapi.info["default_mount"]["s3"]:
            name = s3.get("name", "")
            if len(name) == 0 or name in s3_buckets:
                name = s3["id"]
            s3_buckets[name] = s3["path"]

        for external_s3 in self.openapi.mounts["s3"]:
            name = external_s3.get("name", "")
            if len(name) == 0 or name in s3_buckets:
                name = external_s3["id"]
            if name in s3_buckets:
                name = f"{name} - External AWS"
            s3_buckets[name] = external_s3["path"]

        for internal_s3 in self.openapi.s3:
            name = internal_s3["map_settings"].get("name", "")
            if len(name) == 0 or name in s3_buckets:
                name = internal_s3["map_settings"]["id"]
            if name in s3_buckets:
                name = f"{name} - Internal AWS"
            s3_buckets[name] = internal_s3["map_settings"]["path"]

        return s3_buckets

    def listdir(
        self,
        path: str,
        ignore_hidden: bool = True,
        get_details: bool = False,
    ) -> Union[List[Dict[str, Union[str, int, dict]]], List[str]]:
        """
        List all files and folders with path in domain server

        Parameters
        ----------
        path: ``str``
            path of folder to list
        ignore_hidden: ``bool``, default: True
            Ignore hidden files/folders or not
        get_details: ``bool``, default: False
            Get details information or not

        Returns
        -------
        results: ``Union[List[Dict[str, Union[str, int, dict]]], List[str]]``
            Folders and files with their information
        """
        dir_elements = self.openapi.list_dir(
            path, ignore_hidden=ignore_hidden
        )[ConnectorKeys.ENTITIES.value]
        if get_details:
            return dir_elements
        return [element[ConnectorKeys.NAME.value] for element in dir_elements]

    def parse_data_information(self, data_name: str, technology: str, data_path: str) -> dict:
        """
        Parse information of data to valid format for submission

        Parameters
        ----------
        data_name: ``str``
            Name of spatial data
        technology: ``str``
            Technology of spatial data
        data_path: ``str``
            Path to spatial data

        Returns
        -------
        submission_data: ``dict``
            Auto-detect information for submission
        """
        return self.pyapi.parse_data_information(data_name, technology, data_path)

    def parse_multiple_samples_information(
        self,
        technology: str,
        data_path: str,
        sample_name_mapping: dict = {},
        data_name_mapping: dict = {},
    ) -> List[dict]:
        """
        Parse information of multiple samples to valid format for submission

        Parameters
        ----------
        technology: ``str``
            Technology of spatial data
        data_path: ``str``
            Path to spatial data

        Returns
        -------
        submission_samples: ``dict``
            Auto-detect information for submission
        """
        results: List[dict] = []
        for folder in self.listdir(data_path, get_details=True):
            if folder[ConnectorKeys.TYPE.value] != ConnectorKeys.DIRECTORY.value:
                continue
            try:
                data = self.pyapi.parse_data_information(
                    data_name_mapping.get(folder[ConnectorKeys.NAME.value], folder[ConnectorKeys.NAME.value]),
                    technology,
                    os.path.join(data_path, folder[ConnectorKeys.NAME.value]),
                )
                results.append({
                    ConnectorKeys.SAMPLE_NAME.value: sample_name_mapping.get(
                        folder[ConnectorKeys.NAME.value], folder[ConnectorKeys.NAME.value]
                    ),
                    ConnectorKeys.DATA.value: data,
                })
            except Exception as e:
                print(f"Fail to parse data in {folder[ConnectorKeys.NAME.value]}: {e}")

        return results

    def list_study(
        self, group: str, species: str, **kwargs
    ) -> Dict[str, Union[str, dict, List[dict]]]:
        """
        List reachable studies

        Parameters
        ----------
        group: ``str``
            Group of studies
        species: ``str``
            Species of studies

        Returns
        -------
        results: ``Dict[str, Union[str, dict, List[dict]]]``
            List of studies and their information

        Keyword Arguments
        -----------------
        limit: ``int``, default: 50
            Limit of responsing data
        offset: ``int``, default: 50
            Starting point of responsing data
        """
        return self.openapi.list_study(self.groups[group], species, **kwargs)["list"]

    def get_study_detail(self, study_id: str, **kwargs) -> Dict[str, Union[str, dict, List[dict]]]:
        """
        Get details information of study

        Parameters
        ----------
        study_id: ``str``
            Id of study

        Returns
        -------
        results: ``Dict[str, Union[str, dict, List[dict]]]``
            Information of study

        Keyword Arguments
        -----------------
        limit: ``int``, default: 50
            Limit of responsing data
        offset: ``int``, default: 50
            Starting point of responsing data
        """
        return self.openapi.get_study_detail(study_id, **kwargs)

    def list_sample(self, study_id: str, **kwargs) -> Dict[str, Union[str, dict, List[dict]]]:
        """
        List samples in a study

        Parameters
        ----------
        study_id: ``str``
            Id of study

        Returns
        -------
        results: ``Dict[str, Union[str, dict, List[dict]]]``
            List of samples and their information

        Keyword Arguments
        -----------------
        limit: ``int``, default: 50
            Limit of responsing data
        offset: ``int``, default: 50
            Starting point of responsing data
        """
        return self.openapi.list_sample(study_id, **kwargs)["list"]

    def get_sample_detail(self, sample_id: str, **kwargs) -> Dict[str, Union[str, dict, List[dict]]]:
        """
        Get details information of sample

        Parameters
        ----------
        sample_id: ``str``
            Id of sample

        Returns
        -------
        results: ``Dict[str, Union[str, dict, List[dict]]]``
            Information of sample

        Keyword Arguments
        -----------------
        limit: ``int``, default: 50
            Limit of responsing data
        offset: ``int``, default: 50
            Starting point of responsing data
        """
        return self.openapi.get_sample_detail(sample_id, **kwargs)

    def get_sample_data_detail(self, data_id: str, **kwargs) -> Dict[str, Union[str, dict, List[dict]]]:
        """
        Get details information of sample data

        Parameters
        ----------
        data_id: ``str``
            Id of data

        Returns
        -------
        results: ``Dict[str, Union[str, dict, List[dict]]]``
            Information of data

        Keyword Arguments
        -----------------
        limit: ``int``, default: 50
            Limit of responsing data
        offset: ``int``, default: 50
            Starting point of responsing data
        """
        return self.openapi.get_sample_data_detail(data_id, **kwargs)

    def get_sample_data_elements(self, data_id: str) -> Dict[str, List[str]]:
        """
        Get elements of sample data

        Parameters
        ----------
        data_id: ``str``
            Id of data

        Returns
        -------
        results: ``Dict[str, List[str]]``
            Elements of data
        """
        results: Dict[str, Dict[str, dict]] =  \
            self.openapi.get_sample_data_detail(data_id).get("map_submit_result", None)
        if results is None:
            return {}
        elements: Dict[str, List[str]] = {}
        for value in results.values():
            if not isinstance(value, dict):
                continue
            for k, v in value.items():
                if k not in elements:
                    elements[k] = []
                elements[k].extend([v] if isinstance(v, str) else v.values())
        return elements

    def add_sample(
        self,
        study_id: str,
        sample_name: str,
        sample_data: List[dict] = [],
    ) -> Dict[str, Union[str, List[dict]]]:
        """
        Add a sample to a existed study

        Parameters
        ----------
        study_id: ``str``
            Id of study
        sample_name: ``str``
            Sample name
        sample_data: ``List[dict]``, default: []
            List of data in sample, each data is result of ``parse_data_information`` function

        Returns
        -------
        results: ``Dict[str, Union[str, List[dict]]]``
            Submission information
        """

        return self.openapi.create_sample(study_id, sample_name, sample_data)

    def add_sample_data(
        self,
        study_id: str,
        sample_id: str,
        sample_data: List[dict],
    ) -> Dict[str, Union[str, List[dict]]]:
        """
        Add data to a existed sample

        Parameters
        ----------
        study_id: ``str``
            Id of sample's root study
        sample_id: ``str``
            Id of sample
        sample_data: ``List[dict]``
            List of data in sample, each data is result of ``parse_data_information`` function

        Returns
        -------
        results: ``Dict[str, Union[str, List[dict]]]``
            Submission information
        """
        return self.openapi.add_sample_data(study_id, sample_id, sample_data)

    def submit(
        self,
        group: str,
        species: str,
        title: str,
        sample_name: str,
        sample_data: List[dict],
    ) -> Dict[str, Union[str, List[dict]]]:
        """
        Create new study and submit the first sample.

        Parameters
        ----------
        group: ``str``
            Group of study
        species: ``str``
            Species of data in study
        title: ``str``
            Title of study
        sample_name: ``str``
            Sample name
        sample_data: ``List[dict]``
            List of data in sample, each data is result of ``parse_data_information`` function

        Returns
        -------
        results: ``Dict[str, Union[str, List[dict]]]``
            Submission information
        """
        study_id = self.openapi.create_study(self.groups[group], species, title)[ConnectorKeys.STUDY_ID.value]
        return self.add_sample(study_id, sample_name, sample_data)

    def submit_multiple_samples(
        self,
        group: str,
        species: str,
        title: str,
        sample_data: List[dict],
    ) -> List[Dict[str, Union[str, List[dict]]]]:
        """
        Create new study and submit the first sample.

        Parameters
        ----------
        group: ``str``
            Group of study
        species: ``str``
            Species of data in study
        title: ``str``
            Title of study
        sample_data: ``List[dict]``
            List of data in sample, each data is result of ``parse_multiple_samples_information`` function

        Returns
        -------
        results: ``List[Dict[str, Union[str, List[dict]]]]``
            Submission information
        """
        study_id = self.openapi.create_study(self.groups[group], species, title)[ConnectorKeys.STUDY_ID.value]

        results = []
        for sample in sample_data:
            sample_name = sample[ConnectorKeys.SAMPLE_NAME.value]
            data = sample[ConnectorKeys.DATA.value]
            results.append(self.add_sample(study_id, sample_name, data))

        return results

    def add_sample_data_element(
        self,
        title: str,
        study_id: str,
        sample_id: str,
        data_id: str,
        adding_types: List[str],
        paths: Dict[str, str] = {},
        args: Dict[str, str] = {},
    ) -> Dict[str, Union[str, List[dict]]]:
        """
        Create new study and submit the first sample.

        Parameters
        ----------
        title: ``str``
            Title of elements
        study_id: ``str``
            Study ID
        sample_id: ``str``
            Sample ID
        data_id: ``str``
            Data ID
        adding_types: `List[str]`
            Type of element to adding, defined in [
                `spatialx_connector.ExtendImagesSubmission`,
                `spatialx_connector.ExtendSegmentationSubmission`,
                `spatialx_connector.ExtendTrasncriptsSubmission`,
                `spatialx_connector.ExtendExpressionSubmission`,
            ]
        paths: `Dict[str, str]`
            Mapping of elements defined in `spatialx_connector.SubmissionElementKeys` and their paths.
        args: `Dict[str, str]`
            Mapping of elements defined in `spatialx_connector.SubmissionElementKeys` and values.

        Returns
        -------
        results: ``List[Dict[str, Union[str, List[dict]]]]``
            Submission information
        """
        return self.openapi.add_sample_data_element(
            title,
            study_id,
            sample_id,
            data_id,
            identities=adding_types,
            files=[
                {
                    ConnectorKeys.KEY.value: key,
                    ConnectorKeys.VALUE.value: value,
                }
                for key, value in paths.items()
            ],
            args=[
                {
                    ConnectorKeys.KEY.value: key,
                    ConnectorKeys.VALUE.value: value,
                }
                for key, value in args.items()
            ] + [
                {
                    ConnectorKeys.KEY.value: "ignore_technology_elements",  # Ignore default types of technologies.
                    ConnectorKeys.VALUE.value: True,
                }
            ],
        )

    def upload_file(
        self,
        file_path: str,
        server_folder_name: str = "",
        upload_id: str = "",
        is_chunk: bool = False,
    ) -> Dict[str, Union[str, List[dict]]]:
        """
        upload a small file

        Parameters
        ----------
        file_path: ``str``
            File location
        server_folder_name: ``str``
            Folder location in spatialx server
        upload_id: ``str``
            Upload ID

        Returns
        -------
        results: ``Dict[str, Union[str, List[dict]]]``
            Upload information
        """
        return self.openapi.upload_file(
            file_path=file_path,
            folder_name=server_folder_name,
            upload_id=upload_id,
            is_chunk=is_chunk,
        )

    def upload_big_file(
        self,
        file_path: str,
        chunk_size: int = 0,
        debug_mode: bool = False,
        server_folder_name: str = "",
        chunk_resp: dict = {},
        move_to_parent: bool = True,
    ) -> Dict[str, Union[str, List[dict]]]:
        """
        Upload a big file

        Parameters
        ----------
        file_path: ``str``
            File location
        chunk_size: ``int``
            Chunk size (bytes), 0: auto
        debug_mode: ``bool``
            Debug mode
        server_folder_name: ``str``
            Folder location in spatialx server

        Returns
        -------
        results: ``Dict[str, Union[str, List[dict]]]``
            Upload information
        """
        if not os.path.isfile(file_path):
            raise Exception(f"Invalid file: {file_path}")

        file_size = os.stat(os.path.abspath(file_path)).st_size
        upload_id = ""
        resp = chunk_resp
        if ConnectorKeys.UNIQUE_ID.value in resp:
            upload_id = resp[ConnectorKeys.UNIQUE_ID.value]

        # Direct upload if small file
        if file_size < ConnectorKeys.UPLOAD_CHUNK_SMALL_SIZE.value:
            if ConnectorKeys.UNIQUE_ID.value in resp:
                upload_id = resp[ConnectorKeys.UNIQUE_ID.value]

            return self.upload_file(
                file_path=file_path,
                server_folder_name=server_folder_name,
                upload_id=upload_id,
                is_chunk=True,
            )

        file_name = Path(file_path).name
        item_chunk_size = get_chunk_size(chunk_size, file_size)

        if (len(resp.keys()) == 0) or (len(upload_id) == 0):
            resp = self.openapi.upload_chunk_start(
                folder_name=server_folder_name,
                parent_is_file=2,
            )

            if ConnectorKeys.UNIQUE_ID.value in resp:
                upload_id = resp[ConnectorKeys.UNIQUE_ID.value]

        file = open(file_path, "rb")
        file.seek(0, 0)
        sending_index = 0
        offset_size = 0
        progress_bar = None
        if debug_mode:
            progress_bar = tqdm(total=file_size, unit="B", unit_scale=True)

        while True:
            data = file.read(item_chunk_size)
            if not data:
                break

            offset_size = offset_size + item_chunk_size
            offset_size = min(file_size, offset_size)

            if debug_mode:
                format_print(f"Upload {file_path}, chunk index : {sending_index + 1} ...")

            self.openapi.upload_chunk_process(
                chunk_size=item_chunk_size,
                file_size=file_size,
                offset=offset_size,
                file_name=file_name,
                folder_name=server_folder_name,
                upload_id=upload_id,
                path=resp[ConnectorKeys.ROOT_FOLDER.value],
                sending_index=sending_index,
                parent_is_file=2,
                file_data=data,
            )

            if debug_mode:
                if progress_bar is not None:
                    progress_bar.update(len(data))

            sending_index = sending_index + 1

        total_index = sending_index
        file.close()

        resp2 = self.openapi.upload_chunk_merge(
            total_chunk=total_index,
            file_name=file_name,
            folder_name=server_folder_name,
            upload_id=upload_id,
            path=resp[ConnectorKeys.ROOT_FOLDER.value],
            parent_is_file=2,
            move_to_parent=move_to_parent,
        )

        if move_to_parent:
            return resp2
        return resp

    def upload_folder(
        self,
        dir_path: str,
        folder_path: Optional[str] = None,
        chunk_size: int = 0,
        debug_mode: bool = False,
        server_folder_name: str = "",
        chunk_resp: dict = {},
    ) -> bool:
        """
        Upload folder as: zarr

        Parameters
        ----------
        dir_path: ``str``
            Folder location
        chunk_size: ``int``
            Chunk size (bytes), 0: auto
        debug_mode: ``bool``
            Debug mode
        server_folder_name: ``str``
            Folder location in spatialx server
        """
        if not os.path.isdir(dir_path):
            raise Exception(f"Invalid directory: {dir_path}")

        root_folder_path = ""
        if folder_path is None:
            folder_path = server_folder_name + os.path.basename(dir_path)
            root_folder_path = str(folder_path)

        src_path = Path(dir_path)
        resp = chunk_resp

        for src_child in src_path.iterdir():
            if src_child.is_dir():
                folder_path = os.path.join(folder_path, src_child.stem)
                dst_child = os.path.join(dir_path, src_child.stem)
                self.upload_folder(
                    dir_path=dst_child, folder_path=folder_path,
                    chunk_size=chunk_size, debug_mode=debug_mode,
                    server_folder_name=server_folder_name,
                    chunk_resp=resp,
                )
            else:
                if src_child.is_symlink():
                    continue

                dst_child = os.path.join(dir_path, src_child.name)
                resp = self.upload_big_file(
                    file_path=dst_child,
                    chunk_size=chunk_size,
                    debug_mode=debug_mode,
                    server_folder_name=folder_path,
                    chunk_resp=resp,
                    move_to_parent=False,
                )

        return self.openapi.upload_folder_finish(
            root_folder_path,
            resp[ConnectorKeys.UNIQUE_ID.value],
        )

    def list_lens_bulk_studies(self, host: str, token: str, group: str, species: str):
        from bioturing_connector.lens_bulk_connector import LensBulkConnector

        connector = LensBulkConnector(host=host, token=token, ssl=True)
        connector.test_connection()
        if group == DefaultGroup.PERSONAL_WORKSPACE.value:
            group_id = DefaultGroup.LENS_GROUP_ID_PERSONAL_WORKSPACE.value
        elif group == DefaultGroup.ALL_MEMBERS.value:
            group_id = DefaultGroup.LENS_GROUP_ID_ALL_MEMBERS.value
        else:
            group_id = self.groups.get(group, group)

        studies_info = connector.get_all_studies_info_in_group(group_id=group_id, species=species)
        studies_info = [
            {
                **info,
                ConnectorKeys.SPECIES.value: species,
                ConnectorKeys.GROUP_ID.value: self.groups.get(
                    group, DefaultGroup.PERSONAL_WORKSPACE.value
                ),
            }
            for info in studies_info
        ]
        return studies_info

    def list_lens_sc_studies(self, host: str, token: str, group: str, species: str):
        from bioturing_connector.lens_sc_connector import LensSCConnector

        connector = LensSCConnector(host=host, token=token, ssl=True)
        connector.test_connection()
        if group == DefaultGroup.PERSONAL_WORKSPACE.value:
            group_id = DefaultGroup.LENS_GROUP_ID_PERSONAL_WORKSPACE.value
        elif group == DefaultGroup.ALL_MEMBERS.value:
            group_id = DefaultGroup.LENS_GROUP_ID_ALL_MEMBERS.value
        else:
            group_id = self.groups[group]

        studies_info = connector.get_all_studies_info_in_group(group_id=group_id, species=species)
        studies_info = [
            {
                **info,
                ConnectorKeys.SPECIES.value: species,
                ConnectorKeys.GROUP_ID.value: self.groups[group],
            }
            for info in studies_info
        ]
        return studies_info

    def convert_data_from_lens(self, study_info: Union[dict, List[dict]]):
        if isinstance(study_info, dict):
            study_info = [study_info]

        for info in study_info:
            self.openapi.convert_from_lens(
                f"ST-{info['id']}",
                info["title"],
                info[ConnectorKeys.GROUP_ID.value],
                info[ConnectorKeys.SPECIES.value],
                info["id"],
            )
