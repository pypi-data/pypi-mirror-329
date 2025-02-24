import os
import sys
import time
import json
import uuid
from pathlib import Path
from typing import Dict, List, Optional, Union
import pandas as pd

import pkg_resources
from tqdm import tqdm

from ._api import Connector, OpenAPI
from ._constants import ConnectorKeys, PLATFORM
from ._utils import format_print, get_chunk_size


class SmartbulkConnector(Connector):
    """
    Smartbulk Connector
    Supporting to work with smartbulk data via notebook.
    """

    def __init__(self, domain: str, token: str, verify_ssl: bool = False):
        """
        Construct parameters for train and query k-nearest neighbors

        Parameters
        ----------
        domain: ``str``
            smartbulk domain
        token: ``str``
            User's token
        verify_ssl: ``bool``, default: False
            Verify SSL or not.
        """
        super().__init__(domain, token, verify_ssl)
        self.__openapi = OpenAPI(domain, token, verify_ssl)
        self.__check_connection
    
    @property
    def openapi(self) -> OpenAPI:
        return self.__openapi

    @property
    def info(self):
        """Current user's information"""
        info = self.openapi.info
        return {
            field: info[field]
            for field in ConnectorKeys.INFORMATION_FIELDS
        }
    
    @property
    def personal_group_id(self):
        """Return personal group id"""
        group_id = next(
            (
                group['group_id'] for group in self.get_user_groups() if group['group_name'] == 'Personal workspace'
            ), 
            None
        )
        return group_id

    @property
    def groups(self):
        """List all reachable groups of current user in domain server."""
        return self.openapi.groups
    
    @property
    def __check_connection(self):
        try:
            print(f'Connecting to host at {self._domain}')
            self.info['email']
            print('Connect to SmartBulk successfully')
        except Exception as e:
            print(str(e))
            print("Cannot connect to the domain, please verify your domain and your token!")
    
    def get_user_groups(self):
        """
        Get all available groups of current token

        Returns
        ----------
        List of groups' info : List[dict]
        In which:
            'group_id': uuid of the group, which will be used in further steps,\n
            'group_name': displaying name of the group
        """
        res = self.openapi.groups
        data = []

        for group_id in res['default']:
            data.append({'group_id': group_id, 'group_name': res['default'][group_id]})

        for group in res['groups']:
            data.append({'group_id': group['id'], 'group_name': group['name']})
        return data

    def get_all_projects_info_in_group(self, group_id: str, limit: int = 100, offset: int = 0, active: bool = True):
        """
        Get all project info in a group

        Parameters
        ----------
        group_id: ``str``
            group id of groups
        limit: ``int``
            print only n_limit
        offset: ``int``
            begin with the k_offset project'
        active: ``bool``
            turn on/off displaying inactive/deleted projects
        
        Returns
        ----------
        List of projects info: ``List[dict]``
        """
        if group_id == 'personal':
            group_id = self.personal_group_id

        if not self.validate_group_id(group_id=group_id):
            return None

        project_params = {
            "limit": limit,
            "offset": offset,
            "group_id": group_id,
            "activate": int(active),
        }

        res = self.openapi.list_projects(json=project_params)
        data = []
        for project in res:
            data.append({
                'project_id': project['project_id'],
                'project_name': project['project_name']
            })
        return data

    @property
    def external_mounts(self):
        """List all reachable mounted shared folders of current user from BBrowserX/BioStudio."""
        return {
            folder["name"]: folder["path"]
            for folder in self.openapi.mounts["s3"]
        }

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
        defaults = {
            folder["name"]: folder["path"]
            for folder in self.openapi.info["default_mount"]["s3"]
        }
        return dict(self.external_mounts.items() | defaults.items())
    
    def get_user_s3(self):
        """
        Get all available groups of current token

        Returns
        -------
        List of s3 bucket' info : List[dict]
        In which:
            'id': uuid of the s3 bucket, which will be used in further steps
            'bucket': bucket of s3
            'prefix': prefix of s3
            'mount_point': s3://[bucket]/[prefix]/
        """
        res = self.openapi.get_user_s3
        list_buckets = []
        for s3_info in res:
            s3 = s3_info['map_settings']
            list_buckets.append({
                'id': s3['id'],
                'bucket': s3['bucket'],
                'prefix': s3['prefix'],
                'mount_point': s3['mount_point'],
            })
        return list_buckets

    def get_versions(self):
        sdk_version = pkg_resources.get_distribution("smartbulk_connector").version
        print(f'smartbulk_connector: version ' + sdk_version)

    @property
    def get_base_dir(self):
        """
        Get current working directory in the SmarBulk Server
        """
        base_dir = self.openapi.info['default_mount']['folders'][0]['path']
        base_dir = os.path.dirname(base_dir)
        return base_dir

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
        )[ConnectorKeys.ENTITIES]
        if get_details:
            return dir_elements
        return [element[ConnectorKeys.NAME] for element in dir_elements]

    def listdir_server(
            self, 
            path: str = '',
            storage: str = 'upload',
            ignore_hidden: bool = True,
            get_details: bool = False,
            fullpath: bool = False,
        ) -> Union[List[Dict[str, Union[str, int, dict]]], List[str]]:
        """
        List all files and directories in the SmarBulk Server

        Parameters
        ----------
        path: ``str``
            path of folder to list
        storage: ``str``, default: 'upload'
            Storatge type (e.g, 'upload', 'cloud_storages')
        ignore_hidden: ``bool``, default: True
            Ignore hidden files/folders or not
        get_details: ``bool``, default: False
            Get details information or not
        fullpath: ``bool``, default: False


        Returns
        -------
        results: ``Union[List[Dict[str, Union[str, int, dict]]], List[str]]``
            Folders and files with their information
        """
        base_dir = self.get_base_dir
        # os.path.join return different format in windows
        current_dir = '/'.join([base_dir, storage]) 
        file_path = '/'.join([current_dir, path])

        try:
            res = self.listdir(
                path=file_path, 
                ignore_hidden=ignore_hidden, 
                get_details=get_details,
            )
        except:
            return []

        if get_details:
            return res
        
        format_res = []
        for element in res:
            if fullpath:
                # os.path.join return different format in windows
                element = '/'.join([file_path, element])
            format_res.append(element)
        return format_res

    def listdir_cloud_storage(
            self, 
            path: str = '',
            ignore_hidden: bool = True,
            get_details: bool = False,
            fullpath: bool = False,
        ) -> Union[List[Dict[str, Union[str, int, dict]]], List[str]]:
        """
        List all files and directory in the cloud storage in the SmarBulk Server
        """
        return self.listdir_server(
            path=path,
            storage='cloud_storages',
            ignore_hidden=ignore_hidden,
            get_details=get_details,
            fullpath=fullpath
        )
    
    def listdir_workspace(
            self, 
            path: str = '',
            ignore_hidden: bool = True,
            get_details: bool = False,
            fullpath: bool = False,
        ) -> Union[List[Dict[str, Union[str, int, dict]]], List[str]]:
        """
        List all files and directory in the workspace in the SmarBulk Server
        """
        return self.listdir_server(
            path=path,
            storage='upload',
            ignore_hidden=ignore_hidden,
            get_details=get_details,
            fullpath=fullpath
        )

    def validate_recipes(self, recipe_path: str):
        extension = os.path.splitext(recipe_path)[1]
        if extension == '.csv':
            df = pd.read_csv(recipe_path)
        elif extension == '.tsv':
            df = pd.read_csv(recipe_path, sep='\t')
        else:
            raise ValueError("recipes file must be either .csv or .tsv")
        datasets = {}
        grouped = df.groupby('dataset_name')
        for dataset_name, group in grouped:
            species = group['species'].unique()
            if len(species) > 1:
                raise ValueError(f"Species mismatch in dataset {dataset_name}")
            species = species[0]

            platform = group['platform'].unique()
            if len(platform) > 1:
                raise ValueError(f"Platform mismatch in dataset {dataset_name}")
            platform = platform[0]
            
            if platform == 'bulk':
                metadata_paths = group.loc[group['file_type'] == 'metadata', 'path_on_server'].tolist()
                matrix_paths = group.loc[group['file_type'] == 'matrix', 'path_on_server'].tolist()
                
                if not metadata_paths:
                    raise ValueError(f"Dataset {dataset_name} is missing a metadata file.")
                if not matrix_paths:
                    raise ValueError(f"Dataset {dataset_name} is missing a matrix file.")
                
                datasets[dataset_name] = {
                    'dataset_name': dataset_name,
                    'rcc_folder_path': '',
                    'metadata_paths': metadata_paths,
                    'matrix_paths': matrix_paths,
                    'species': species,
                    'platform': platform
                }
            elif platform == 'nanostring':
                rcc_folder_path = group.loc[group['file_type'] == 'rcc', 'path_on_server'].tolist()
                metadata_paths = group.loc[group['file_type'] == 'metadata', 'path_on_server'].tolist()
                matrix_paths = group.loc[group['file_type'] == 'matrix', 'path_on_server'].tolist()

                if rcc_folder_path:
                    pass
                elif not rcc_folder_path and not matrix_paths:
                    raise ValueError(f"Dataset {dataset_name} is missing a rcc folder.")
                elif not matrix_paths and not metadata_paths:
                    raise ValueError(f"Dataset {dataset_name} is missing a metadata file.")
                
                if len(rcc_folder_path) > 0:
                    rcc_path = rcc_folder_path[0]
                else:
                    rcc_path = ''
                
                datasets[dataset_name] = {
                    'dataset_name': dataset_name,
                    'rcc_folder_path': rcc_path,
                    'metadata_paths': metadata_paths,
                    'matrix_paths': matrix_paths,
                    'species': species,
                    'platform': platform
                }

        result = list(datasets.values())
        return result
    
    def validate_file_paths(
            self,
            file_paths: List[str]
    ):
        """Validate file_paths for creating project"""
        if isinstance(file_paths, list):
            if len(file_paths) < 1:
                print("Error: matrix_paths/metadata_paths list must a list contains at least one path")
                return False
            
            if len(file_paths) != len(set(file_paths)):
                print("Error: matrix_paths/metadata_paths list contains dupplicate paths, please check again")
                return False
            
            for file_path in file_paths:
                try:
                    self.check_file_exists(file_path)
                    if not file_path.endswith(('.tsv', '.csv', '.csv.gz', '.tsv.gz', '.txt', '.txt.gz')):
                        print(f'Error: file_path: {file_path} file extension is invalid. Support: (csv, tsv, tsv.gz, csv.gz, txt, txt.gz)')
                        return False
                except:
                    print(f"Error: file path: {file_path} is not found on the server")
                    return False
        else:
            print("Error: matrix_paths/metadata_paths list must a list contains at least one path")
            return False
            
        return True

    def __create_project(self,
                   group_id: str,
                   species: str,
                   project_name: str,
                   dataset_name: str,
                   matrix_paths: list[str] = [],
                   metadata_paths: list[str] = [],
                   rcc_folder_path: str = '',
                   project_id: str = '',
                   use_gene_symbols: bool = True,
                   aggregate_count: bool = False,
                   platform: str = 'bulk',
        ) -> Dict[str, Union[str, List[dict]]]:
        sdk_version = str(pkg_resources.get_distribution("smartbulk_connector").version)

        if group_id == 'personal':
            group_id = self.personal_group_id
        
        print('Checking the server files...')
        if platform == 'bulk':
            platform = 0

            if not self.validate_file_paths(matrix_paths + metadata_paths):
                return
            
            return self.openapi.create_project(
                group_id=group_id, 
                species=species, 
                project_name=project_name, 
                matrix_paths=matrix_paths, 
                metadata_paths=metadata_paths, 
                dataset_name=dataset_name, 
                project_id=project_id, 
                use_gene_symbols=use_gene_symbols,
                platform=platform,
                sdk_version=sdk_version,
            )

        elif platform == 'nanostring':
            platform = 1
            matrix_path = ''
            metadata_path = ''

            if rcc_folder_path != '':
                if len(self.listdir(rcc_folder_path)) == 0:
                    print('Error: RCC Folder Path is not found on the working directory')
                    return
                if len(metadata_paths) > 0:
                    if not self.validate_file_paths(metadata_paths[:1]):
                        return
                    metadata_path = metadata_paths[0]
                    
            elif len(matrix_paths) > 0 and len(metadata_paths) > 0:
                if not self.validate_file_paths(matrix_paths[:1] + metadata_paths[:1]):
                    return
                matrix_path = matrix_paths[0]
                metadata_path = metadata_paths[0]

            return self.openapi.create_nanostring_project(
                group_id=group_id,
                species=species,
                project_name=project_name,
                rcc_folder_path=rcc_folder_path,
                matrix_path=matrix_path,
                metadata_path=metadata_path,
                dataset_name=dataset_name,
                project_id=project_id,
                aggregate_count=aggregate_count,
                sdk_version=sdk_version,
                platform=platform,
            )
        else:
            print('Error: platform must be either bulk or nanostring')
            return
    
    def create_project(self,
                   group_id: str,
                   species: str,
                   project_name: str,
                   dataset_name: str,
                   matrix_paths: list[str] = [],
                   metadata_paths: list[str] = [],
                   rcc_folder_path: str = '',
                   use_gene_symbols: bool = True,
                   aggregate_count: bool = False,
                   platform: str = 'bulk',
        ) -> Dict[str, Union[str, List[dict]]]:
        """
        Create a new project and submit the dataset.

        Parameters
        ----------
        group_id : str
            Identifier for the group associated with the project.
        species : str
            The species from which the project data is derived.
        project_name : str
            Name of the project being created.
        matrix_paths : list[str]
            List of file paths to matrix data related to the project.
        metadata_paths : list[str]
            List of file paths to metadata associated with the project.
        dataset_name : str
            Name of the dataset for the project.
        project_id: str
            Identifier for the project.
        use_gene_symbols: bool
            Convert genes from matrix using gene symbols.

        Returns
        -------
        Dict[str, Union[str, List[dict]]]
            A dictionary containing submission details, including project ID 
            and any relevant metadata.

        """
        return self.__create_project(
            project_id='',
            group_id=group_id,
            species=species,
            project_name=project_name,
            dataset_name=dataset_name,
            matrix_paths=matrix_paths,
            metadata_paths=metadata_paths,
            rcc_folder_path=rcc_folder_path,
            use_gene_symbols=use_gene_symbols,
            aggregate_count=aggregate_count,
            platform=platform,
        )
    
    def validate_group_id(self, group_id: str):
        """Check group_id"""
        list_group_id = [info['group_id'] for info in self.get_user_groups()]
        if group_id not in list_group_id:
            print(f"Error: Group ID: {group_id} not found in your workspace")
            return False
        
        return True

    
    def validate_project_id(self, project_id: str, group_id: str):
        """Check group_id and project_id"""
        if not self.validate_group_id(group_id=group_id):
            return None
        
        dict_project_info = self.get_all_projects_info_in_group(group_id)
        list_project_id_in_group = [
            info['project_id'] for info in dict_project_info
        ]
        if project_id not in list_project_id_in_group:
            print(f"Error: Project ID: {project_id} not found in group {group_id}")
            return None
        
        index = list_project_id_in_group.index(project_id)
        project_name = dict_project_info[index]['project_name']
        return project_name
    
    def add_project(
        self,
        project_id: str,
        group_id: str,
        species: str,
        dataset_name: str,
        matrix_paths: list[str] = [],
        metadata_paths: list[str] = [],
        rcc_folder_path: str = '',
        use_gene_symbols: bool = True,
        aggregate_count: bool = False,
        platform: str = 'bulk',
    ):
        """
        Add dataset to a project using project_id

        Parameters
        ----------
        project_id: str
            Identifier for the project.
        group_id: str
            Identifier for the group associated with the project.
        species: str
            The species from which the project data is derived.
        matrix_paths : list[str]
            List of file paths to matrix data related to the project.
        metadata_paths : list[str]
            List of file paths to metadata associated with the project.
        use_gene_symbols: bool
            Convert genes from matrix using gene symbols.
        """
        if group_id == 'personal':
            group_id = self.personal_group_id

        project_name = self.validate_project_id(project_id=project_id, group_id=group_id)
        if not project_name:
            return 
        
        return self.__create_project(
            project_id=project_id,
            group_id=group_id,
            species=species,
            project_name=project_name,
            dataset_name=dataset_name,
            matrix_paths=matrix_paths,
            metadata_paths=metadata_paths,
            rcc_folder_path=rcc_folder_path,
            use_gene_symbols=use_gene_symbols,
            aggregate_count=aggregate_count,
            platform=platform,
        )

    
    def __create_project_from_recipes(
            self, 
            group_id: str, 
            recipes_path: str,
            project_name: str,
            project_id: str = '',
            trace_log: str = '',
            use_gene_symbols: bool = True,
            aggregate_count: bool = False,
        ):
        if not os.path.isfile(recipes_path):
            raise Exception(f"File not found: {recipes_path}")

        if group_id == 'personal':
            group_id = self.personal_group_id

        recipes = self.validate_recipes(recipes_path)

        if project_id == '':
            project_id = f"prj_{uuid.uuid4()}"

        if trace_log == '':
            trace_log_path = os.path.join(project_id, 'project_trace_log.json')
            trace_log_list_json = {
                'project_id': project_id,
                'project_name': project_name,
                'success': [],
                'failed': [],
            }

            os.makedirs(project_id, exist_ok=True)
        else:
            trace_log_path = trace_log
            with open(trace_log_path, 'r') as json_file:
                trace_log_list_json = json.load(json_file)
            project_id = trace_log_list_json['project_id']
        
        for data in recipes:
            dataset_name = data['dataset_name']

            if dataset_name in trace_log_list_json['success']:
                continue

            try:
                submit_resp = self.__create_project(
                    group_id=group_id,
                    species=data['species'],
                    project_name=project_name,
                    matrix_paths=data['matrix_paths'],
                    metadata_paths=data['metadata_paths'],
                    rcc_folder_path=data['rcc_folder_path'],
                    dataset_name=dataset_name,
                    project_id=project_id,
                    use_gene_symbols=use_gene_symbols,
                    aggregate_count=aggregate_count,
                    platform=data['platform'],
                )

                project_status = self.check_project_status(submit_result=submit_resp)
            except Exception as error:
                print("Something went wrong, ", error)
                project_status = False
            
            if project_status:
                trace_log_list_json['success'].append(dataset_name)
                if dataset_name in trace_log_list_json['failed']:
                    trace_log_list_json['failed'].remove(dataset_name)
            else:
                if dataset_name not in trace_log_list_json['failed']:
                    trace_log_list_json['failed'].append(dataset_name)

            with open(trace_log_path, 'w') as json_file:
                json.dump(trace_log_list_json, json_file, indent=4)
    
        return trace_log_list_json

    def create_project_from_recipes(
            self, 
            group_id: str, 
            recipes_path: str,
            project_name: str,
            trace_log: str = '',
            use_gene_symbols: bool = True,
            aggregate_count: bool = False,
        ):
        """
        Create a new project with multiple dataset using recipes
        This recipes file is a csv file that includes: 
            dataset_name: one or many datasets, a dataset must contains matrix and metadata
            path_on_server: server path to the file in one dataset
            file_type: can be either matrix or metadata, identify the path_on_server type
            species: can be either human or mouse

        Parameters
        ----------
        group_id: ``str``
            Group of project
        recipes_path: ``str``
            Path to the recipes file
        project_name: ``str``
            Name of the project
        trace_log: ``str``
            Path to the tracelog file
        use_gene_symbols: ``bool``
            Convert genes from matrix using gene symbols.
        """
        return self.__create_project_from_recipes(
            group_id=group_id,
            recipes_path=recipes_path,
            project_name=project_name,
            project_id='',
            trace_log=trace_log,
            use_gene_symbols=use_gene_symbols,
            aggregate_count=aggregate_count,
        )

    def add_project_from_recipes(
            self,
            project_id: str,
            group_id: str, 
            recipes_path: str,
            trace_log: str = '',
            use_gene_symbols: bool = True,
            aggregate_count: bool = False,
    ):
        if group_id == 'personal':
            group_id = self.personal_group_id

        project_name = self.validate_project_id(project_id=project_id, group_id=group_id)
        if not project_name:
            return
        
        return self.__create_project_from_recipes(
            group_id=group_id,
            recipes_path=recipes_path,
            project_name=project_name,
            project_id=project_id,
            trace_log=trace_log,
            use_gene_symbols=use_gene_symbols,
            aggregate_count=aggregate_count,
        )
        

    def check_project_status(self, submit_result: str, log_file: str = ''):
        """
        Waits and print the project submission log file until project status is 'Done' or 'Error'

        Parameters
        ----------
        submit_result: ``dict``
            Either create project or add project result log
        log_file: ``str``
            The path to the log file.

        Returns
        ----------
        Bool
            True if submission success
            Error if submission fail
        return: True if 'Done' or 'Error' is found in the log, False if timeout is reached.
        """
        if log_file == '': 
            submit_result = json.loads(submit_result)
            log_file = submit_result['msg']['message']['log_file']
            project_id = submit_result['msg']['message']['project_id']
        else:
            project_id = ''

        print(f'============== Create Project Log ==============')
        print(f'Project ID: {project_id}')

        start_time = time.time()
        while time.time() - start_time < 1800: # 30 minutes
            log_content = self.get_file_content(path=log_file)
            print(log_content, flush=True, end="\r")
            if 'Done' in log_content:
                print('================================================')
                return True
            if 'Error' in log_content or 'ERROR' in log_content:
                return False
            time.sleep(2)  # Wait before checking again
        
        print('Create Project Log takes very long time. STOP CHECKING!')
        return False

    def get_file_content(self, path: str) -> str:
        return self.openapi.get_file_content(
            path
        )
    
    def check_file_exists(self, path: str):
        return self.openapi.check_file_exists(path)

    def print_file_content(self, path: str) -> None:
        content = self.get_file_content(path)
        print("Content: " + content)
        if len(path) == 0:
            return
        while True:
            try:
                content = self.get_file_content(path)
                print(content)
                break
                sys.stdout.flush()
                time.sleep(1)
            except:
                break

    def submit(
        self,
        group_id: str,
        species: str,
        title: str,
        sample_name: str,
        sample_data: List[dict],
    ) -> Dict[str, Union[str, List[dict]]]:
        """
        Create new study and submit the first sample.

        Parameters
        ----------
        group_id: ``str``
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
        study_id = self.openapi.create_study(
            group_id, species, title
        )[ConnectorKeys.STUDY_ID]

        return self.add_sample(study_id, sample_name, sample_data)

    def __upload_file(
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
            Folder location in smartbulk server
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

    def upload_file(
        self,
        file_path: str,
        chunk_size: int = 0,
        debug_mode: bool = False,
        server_folder_name: str = "",
        chunk_resp: dict = {},
        move_to_parent: bool = True,
    ) -> Dict[str, Union[str, List[dict]]]:
        """
        Upload a file to server workspace

        Parameters
        ----------
        file_path: ``str``
            File location
        chunk_size: ``int``
            Chunk size (bytes), 0: auto
        debug_mode: ``bool``
            Debug mode
        server_folder_name: ``str``
            Folder location in smartbulk server

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
        if ConnectorKeys.UNIQUE_ID in resp:
            upload_id = resp[ConnectorKeys.UNIQUE_ID]

        # Direct upload if small file
        if file_size < ConnectorKeys.UPLOAD_CHUNK_SMALL_SIZE:
            if ConnectorKeys.UNIQUE_ID in resp:
                upload_id = resp[ConnectorKeys.UNIQUE_ID]

            return self.__upload_file(
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

            if ConnectorKeys.UNIQUE_ID in resp:
                upload_id = resp[ConnectorKeys.UNIQUE_ID]

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
                format_print(
                    f"Upload {file_path}, chunk index : {sending_index + 1} ...")

            self.openapi.upload_chunk_process(
                chunk_size=item_chunk_size,
                file_size=file_size,
                offset=offset_size,
                file_name=file_name,
                folder_name=server_folder_name,
                upload_id=upload_id,
                path=resp[ConnectorKeys.ROOT_FOLDER],
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
            path=resp[ConnectorKeys.ROOT_FOLDER],
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
        trace_log: str = '',
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
            Folder location in smartbulk server
        """
        if not os.path.isdir(dir_path):
            raise Exception(f"Invalid directory: {dir_path}")
        
        if server_folder_name == "":
            server_folder_name = os.path.basename(dir_path.rstrip('/'))
        
        if trace_log == "":
            trace_id = "upload_folder_" + server_folder_name
            trace_log_path = os.path.join(trace_id, 'upload_trace_log.json')
            trace_log_list_json = {
                'folder_name': server_folder_name,
                'file_path': [],
                'server_path': [],
                'failed': [],
            }

            os.makedirs(trace_id, exist_ok=True)
        else:
            trace_log_path = trace_log
            with open(trace_log_path, 'r') as json_file:
                trace_log_list_json = json.load(json_file)

        root_folder_path = ""
        if folder_path is None:
            folder_path = server_folder_name
            root_folder_path = str(folder_path)

        src_path = Path(dir_path)

        for src_child in src_path.iterdir():
            if src_child.is_dir():
                trace_log_list_json['failed'].append(src_child)

                folder_path = os.path.join(folder_path, src_child.stem)
                dst_child = os.path.join(dir_path, src_child.stem)
                self.upload_folder(
                    dir_path=dst_child, folder_path=folder_path,
                    chunk_size=chunk_size, debug_mode=debug_mode,
                    server_folder_name=server_folder_name,
                    chunk_resp=chunk_resp,
                )

                trace_log_list_json['failed'].remove(src_child) 
            else:
                if src_child.is_symlink():
                    continue

                dst_child = os.path.join(dir_path, src_child.name)
                if dst_child in trace_log_list_json['file_path']:
                    continue
                
                trace_log_list_json['failed'].append(dst_child)
                try:
                    resp = self.upload_file(
                        file_path=dst_child,
                        chunk_size=chunk_size,
                        debug_mode=debug_mode,
                        server_folder_name=folder_path,
                        chunk_resp=chunk_resp,
                        move_to_parent=True,
                    )

                    trace_log_list_json['file_path'].append(dst_child)
                    trace_log_list_json['server_path'].append(resp['path'])
                    if dst_child in trace_log_list_json['failed']:
                        trace_log_list_json['failed'].remove(dst_child) 
                except:
                    pass

        with open(trace_log_path, 'w') as json_file:
            json.dump(trace_log_list_json, json_file, indent=4)
        
        try:
            self.openapi.upload_folder_finish(
                root_folder_path,
                root_folder_path,
            )
        except:
            pass

        if len(trace_log_list_json['failed']) == 0:
            trace_log_list_json.pop('failed', None)

        return trace_log_list_json