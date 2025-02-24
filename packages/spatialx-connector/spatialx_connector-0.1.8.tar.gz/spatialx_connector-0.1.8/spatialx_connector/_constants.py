from enum import Enum


V1_API: str = "pyapi/v1"
OPEN_API: str = "openapi"
TOKEN_KEY: str = "SpatialX-Token"


# PyAPI
SUBMIT_URL: str = "submission/submit_data"
ADD_URL: str = "data_extend/add"
PARSE_DATA_URL: str = "submission/parse_data_information"

SAMPLE_INFO_URL: str = "connector/get_sample_info"

# OpenAPI
INFO_URL: str = "account/info"
GROUPS_URL: str = "account/groups"
LIST_URL: str = "directory/entities"
EXTERNAL_MOUNT_URL: str = "mount/external_listing"
LIST_S3: str = "cloud/setting_list"

CREATE_STUDY_URL: str = "study/create"
LIST_STUDY_URL: str = "study/list"
LIST_PUBLIC_STUDY_URL: str = "study/list_public"
DETAIL_STUDY_URL: str = "study/detail"

CREATE_SAMPLE_URL: str = "sample/create"
LIST_SAMPLE_URL: str = "sample/list"
DETAIL_SAMPLE_URL: str = "sample/detail"

DETAIL_SAMPLE_DATA_URL: str = "data/detail"

ADD_SAMPLE_DATA_URL: str = "data/create"
ADD_SAMPLE_DATA_ELEMENT_URL: str = "data/add_element"

UPLOAD_FILE_URL: str = "upload/simple"
UPLOAD_CHUNK_START_URL: str = "upload/chunk/start"
UPLOAD_CHUNK_PROCESS_URL: str = "upload/chunk/process"
UPLOAD_CHUNK_MERGE_URL: str = "upload/chunk/merge"
UPLOAD_CHUNK_FINISH_URL: str = "upload/chunk/finish"
UPLOAD_FOLDER_FINISH_URL: str = "upload/folder_finish"


# Convert from Lens
STUDY_CONVERT_FROM_LENS_URL: str = "study/convert_from_lens"

# Analysis
CREATE_ANALYSIS_URL: str = "analysis/create"
GET_ANNOTATED_ELEMENTS: str = "metadata/get_annotated_element"


# Types
class Technologies(Enum):
    COSMX_VER1 = "COSMX_VER1"
    COSMX_VER2 = "COSMX_VER2"
    MERSCOPE_VER1 = "MERSCOPE_VER1"
    MERSCOPE_VER2 = "MERSCOPE_VER2"
    XENIUM = "XENIUM"
    XENIUM_HE = "XENIUM_HE"
    VISIUM = "VISIUM"
    VISIUM_HD = "VISIUM_HD"
    SPATIALDATA_ZARR = "SPATIALDATA_ZARR"
    SPATIALDATA_H5AD = "SPATIALDATA_H5AD"


class Species(Enum):
    HUMAN = "human"
    MOUSE = "mouse"
    OTHERS = "others"
    NON_HUMAN_PRIMATE = "nonHumanPrimate"


class StudyType(Enum):
    SINGLECELL_STUDY_TYPE_NUMBER = 0
    SPATIAL_STUDY_TYPE_NUMBER = 1


class StudyStatus(Enum):
    CREATED_STATUS = 0
    SUCCESS_STATUS = 1
    PROCESSING_STATUS = 2
    DELETE_STATUS = 3


class StudyFilter(Enum):
    EQUAL = 0
    NOT_LARGER = 1
    LARGER = 2


class DefaultGroup(Enum):
    PERSONAL_WORKSPACE = "Personal workspace"
    ALL_MEMBERS = "All members"

    LENS_GROUP_ID_PERSONAL_WORKSPACE = "personal"
    LENS_GROUP_ID_ALL_MEMBERS = "all_members"


class ExtendImagesSubmission(Enum):
    TIFFFILE = "IMAGES_TIFFFILE"
    TIFFFILE_3D = "IMAGES_TIFFFILE_3D"
    EXISTED_IMAGES = "IMAGES_FROM_EXISTED"
    EXISTED_PROTEIN_IMAGES = "IMAGES_PROTEIN_FROM_EXISTED"


class ExtendSegmentationSubmission(Enum):
    PARQUET = "SEGMENTATION_PARQUET"
    GEOJSON = "SEGMENTATION_GEOJSON"
    FEATHER = "SEGMENTATION_FEATHER"
    HALO = "SEGMENTATION_HALO"
    CELL_MASKS = "SEGMENTATION_CELL_MASKS"

    FROM_EXISTED = "SEGMENTATION_FROM_EXISTED"
    FROM_IMAGES = "SEGMENTATION_FROM_PROTEIN_IMAGES"


class ExtendTrasncriptsSubmission(Enum):
    DATAFRAME = "TRANSCRIPTS_DATAFRAME"


class ExtendExpressionSubmission(Enum):
    IMPORT_ANNDATA = "IMPORT_ANNDATA"


class SubmissionElementKeys(Enum):
    IMAGES = "images"
    PROTEIN_IMAGES = "protein_images"
    SEGMENTATION = "segmentation"
    TRANSCRIPTS = "transcripts"
    CELL_CENTERS = "cell_centers"
    EXPRESSION = "annotated_data"
    ALIGNMENT = "alignment"

    IMAGES_ID = "images_id"
    SEGMENTATION_ID = "segmentation_id"
    SPATIAL_ID = "spatial_id"
    NUCLEI_CHANNELS = "nuclei_channels"
    MEMBRANE_CHANNELS = "membrane_channels"


class ConnectorKeys(Enum):
    INFORMATION_FIELDS = ["email", "sub_dir", "name", "app_base_url", "routing_table"]

    # Response keys
    ENTITY = "entity"
    ENTITIES = "entities"
    MESSAGE = "message"
    STATUS = "status"
    STUDY = "study"
    SAMPLE = "sample"
    UNIQUE_ID = "unique_id"
    ROOT_FOLDER = "root_folder"

    FILE = "file"
    DIRECTORY = "directory"

    FILES = "files"
    FOLDERS = "folders"
    ARGS = "args"
    IDENTITIES = "identities"

    MAP_SUBMIT_RESULT = "map_submit_result"
    ANNOTATED_DATA = "annotated_data"
    TRANSCRIPTS = "transcripts"
    SPOT = "spot"

    # Parameter keys
    OBS = "obs"
    OBSM = "obsm"
    BARCODES: str = "barcodes"
    GENES: str = "genes"

    STUDY_PATH = "study_path"
    STUDY_ID = "study_id"
    GROUP_ID = "group_id"
    SPECIES = "species"
    LIMIT = "limit"
    OFFSET = "offset"
    ACTIVE = "active"
    COMPARE = "compare"
    NAME = "name"
    DATA = "data"
    DATA_NAME = "data_name"
    SAMPLE_NAME = "sample_name"
    TITLE = "title"
    KEY = "key"
    VALUE = "value"
    TYPE = "type"
    PATH = "path"
    DATA_PATH = "data_path"
    IGNORE_HIDDEN = "ignore_hidden"
    TECHNOLOGY = "technology"
    SAMPLE_ID = "sample_id"
    SAMPLE_DATA = "sample_data"
    SUBMIT_ID = "submit_id"
    SUBMISSION_NAME = "submission_name"
    SUBMISSION_TYPE = "submission_type"
    SUBMISSION_INFO = "submission_info"
    NEED_DATA = "need_data"
    DATA_ID = "data_id"
    TABLE_ID = "table_id"
    LENS_DATA_PATH = "lens_data_path"
    GROUPS = "groups"
    DEFAULT = "default"
    PARAMS = "params"
    DISPLAY_PARAMS = "display_params"
    SUB_TYPE = "sub_type"
    GROUP_TYPE = "group_type"
    DESCRIPTION = "description"
    ELEMENT = "element"

    # Parameter upload keys
    UPLOAD_PARENT_IS_FILE = "parent_is_file"
    UPLOAD_CHUNK_SIZE = "chunk_size"
    UPLOAD_FILE_SIZE = "file_size"
    UPLOAD_OFFSET = "offset"
    UPLOAD_FILE_NAME = "name"
    UPLOAD_FOLDER_NAME = "folder_name"
    UPLOAD_UNIQUE_ID = "unique_id"
    UPLOAD_PATH = "path"
    UPLOAD_MOVE_TO_PARENT = "move_to_parent"
    UPLOAD_SENDING_INDEX = "sending_index"
    UPLOAD_FILE_DATA = "file"
    UPLOAD_TOTAL_CHUNK = "total"
    UPLOAD_IS_CHUNK = "is_chunk"
    UPLOAD_CHUNK_SMALL_SIZE = 1024 * 1024
    UPLOAD_CHUNK_MEDIUM_SIZE = 16 * 1024 * 1024
    UPLOAD_CHUNK_NORMAL_SIZE = 50 * 1024 * 1024
    UPLOAD_CHUNK_LARGE_SIZE = 100 * 1024 * 1024


class NormalizeMethod(Enum):
    RAW = "raw"
    LOG1P_NORMALIZE = "log1p-normalized"
    SQRT_NORMALIZE = "sqrt-normalized"
