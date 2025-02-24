from typing import List

OPEN_API: str = "sdk"
TOKEN_KEY: str = "Smartbulk-Token"

# OpenAPI
INFO_URL: str = "account/info"
GROUPS_URL: str = "account/groups"
PROJECTS_URL: str = "bulk_project/gets"
LIST_URL: str = "directory/entities"
EXTERNAL_MOUNT_URL: str = "mount/external_listing"
LIST_S3: str = "cloud/setting_list"


# Analysis API
CREATE_PROJECT_URL: str = "init_project"
CREATE_NANOSTRING_PROJECT_URL: str = 'init_nanostring_project'
GET_FILE_CONTENT_URL: str = "file/get_content"
CHECK_FILE_EXISTS_URL: str = "file/check"


CREATE_STUDY_URL: str = "study/create"
LIST_STUDY_URL: str = "study/list"
LIST_PUBLIC_STUDY_URL: str = "study/list_public"
DETAIL_STUDY_URL: str = "study/detail"

CREATE_SAMPLE_URL: str = "sample/create"
ADD_SAMPLE_DATA_URL: str = "sample/add_data"
LIST_SAMPLE_URL: str = "sample/list"
DETAIL_SAMPLE_URL: str = "sample/detail"

UPLOAD_FILE_URL: str = "upload/simple"
UPLOAD_CHUNK_START_URL: str = "upload/chunk/start"
UPLOAD_CHUNK_PROCESS_URL: str = "upload/chunk/process"
UPLOAD_CHUNK_MERGE_URL: str = "upload/chunk/merge"
UPLOAD_CHUNK_FINISH_URL: str = "upload/chunk/finish"
UPLOAD_FOLDER_FINISH_URL: str = "upload/folder_finish"

PLATFORM = {
    'bulk': 0,
    'nanostring': 1,
}

class Species:
    HUMAN: str = "human"
    MOUSE: str = "mouse"
    # OTHERS: str = "others"
    # NON_HUMAN_PRIMATE: str = "nonHumanPrimate"

class ConnectorKeys:
    INFORMATION_FIELDS: List[str] = [
        "email", "sub_dir", "name", "app_base_url", "routing_table"
    ]

    # Response keys
    ENTITY: str = "entity"
    ENTITIES: str = "entities"
    MESSAGE: str = "message"
    STATUS: str = "status"
    STUDY: str = "study"
    SAMPLE: str = "sample"
    UNIQUE_ID: str = "unique_id"
    ROOT_FOLDER: str = "root_folder"

    # Parameter keys
    STUDY_PATH: str = "study_path"
    STUDY_ID: str = "study_id"
    GROUP_ID: str = "group_id"
    SPECIES: str = "species"
    LIMIT: str = "limit"
    OFFSET: str = "offset"
    ACTIVE: str = "active"
    COMPARE: str = "compare"
    NAME: str = "name"
    DATA: str = "data"
    DATA_NAME: str = "data_name"
    TITLE: str = "title"
    KEY: str = "key"
    TYPE: str = "type"
    PATH: str = "path"
    FILE: str = "file"
    DATA_PATH: str = "data_path"
    IGNORE_HIDDEN: str = "ignore_hidden"
    TECHNOLOGY: str = "technology"
    SAMPLE_ID: str = "sample_id"
    SUBMIT_ID: str = "submit_id"
    SUBMISSION_NAME: str = "submission_name"
    SUBMISSION_INFO: str = "submission_info"
    NEED_DATA: str = "need_data"

    # Create project keys
    BG_MODE: str = 'bg_mode'
    GROUP_ID: str = 'group_id'
    INIT_OPTION: str = 'init_option'
    INIT_PROJECT_UUID: str = 'init_prj_uuid'
    MATRIX_PATH_LIST:  str = 'matrix_path_list'
    MATRIX_SHEET_LIST: str = 'matrix_sheet_list'
    METADATA_PATH_LIST: str = 'metadata_path_list'
    METADATA_SHEET_LIST: str = 'metadata_sheet_list'
    DATASET_NAME_LIST: str = 'name_list'
    SPECIES: str = 'species'
    PROJECT_NAME: str = 'project_name'
    USE_GENE_SYMBOLS: str = 'convert_gene'
    PLATFORM: str = 'platform'
    SDK_VERSION: str = 'sdk_version'

    # Create Nanostring project keys
    RCC_FOLDER_PATH: str = 'rcc_folder_path'
    AGGREGATE_COUNT: str = 'aggregate_count'

    # Parameter upload keys
    UPLOAD_FOLDER_NAME: str = "folder_name"
    UPLOAD_PARENT_IS_FILE: str = "parent_is_file"
    UPLOAD_CHUNK_SIZE: str = "chunk_size"
    UPLOAD_FILE_SIZE: str = "file_size"
    UPLOAD_OFFSET: str = "offset"
    UPLOAD_FILE_NAME: str = "name"
    UPLOAD_FOLDER_NAME: str = "folder_name"
    UPLOAD_UNIQUE_ID: str = "unique_id"
    UPLOAD_PATH: str = "path"
    UPLOAD_MOVE_TO_PARENT: str = "move_to_parent"
    UPLOAD_SENDING_INDEX: str = "sending_index"
    UPLOAD_FILE_DATA: str = "file"
    UPLOAD_TOTAL_CHUNK: str = "total"
    UPLOAD_IS_CHUNK: str = "is_chunk"
    UPLOAD_CHUNK_SMALL_SIZE: int = 1024 * 1024
    UPLOAD_CHUNK_MEDIUM_SIZE: int = 16 * 1024 * 1024
    UPLOAD_CHUNK_NORMAL_SIZE: int = 50 * 1024 * 1024
    UPLOAD_CHUNK_LARGE_SIZE: int = 100 * 1024 * 1024
