# BioTuring SmartBulk-Connector SDK

Bioturing SmartBulk-Connector SDK is a Python package that provides an interface to interact with Bioturing's services

## Installation

You can install the SmartBulk-Connector SDK package using `pip`:

```bash
pip install --upgrade smartbulk-connector
```

## Get API TOKEN from SmartBulk

An API token is a unique identifier that allows a user or application to access an API. It is a secure way to authenticate a user or application and to control what permissions they have.

You do not need to regenerate your API token every time you use it. However, you may need to regenerate your API token if it is compromised.

Firstly, you need to navigate the SmartBulk SDK to get a token. The user’s token is generated from the host website

## How To Use


```python
import warnings
from smartbulk_connector import SmartbulkConnector

warnings.filterwarnings("ignore")
```

**Connect to SmartBulk private server**


```python
# authentication
DOMAIN = "<your-smartbulk-server-domain>"
TOKEN = "<your-API-token>"
connector = SmartbulkConnector(domain=DOMAIN, token=TOKEN)
```

    Connecting to host at https://dev.bioturing.com/smartbulk
    Connect to SmartBulk successfully


```python
# get current version
connector.get_versions()
```

    smartbulk_connector: version 0.1.0


**Get user groups available for your token**


```python
connector.get_user_groups()
```




    [{'group_id': '<hidden-id>',
      'group_name': 'Personal workspace'},
     {'group_id': '<hidden-id>', 
      'group_name': 'All members'},
     {'group_id': '<hidden-id>',
      'group_name': 'BioTuring Public Studies'}]



**Get all projects from a group**


```python
connector.get_all_projects_info_in_group(group_id='personal')
```


    [{'project_id': 'prj_8dfbc6a8-4e22-444f-b4a2-4df000c48141',
      'project_name': 'sample dataset'},
     {'project_id': 'prj_84c1a392-8080-11ef-8f07-0242ac130004',
      'project_name': 'human sample'},
     {'project_id': 'prj_94f6f0ef-d6c8-49f5-96f6-7bb5fa6a3de8',
      'project_name': 'mouse_sample'}]


**List files and directory in workspace**


```python
connector.listdir_workspace()
```


    ['example_data', 'sample dataset', 'mouse_sample']



```python
connector.listdir_workspace('example_data', fullpath=True)
```


    ['/path/to/server/workspace/upload/example_data/count_mat_2.csv',
     '/path/to/server/workspace/upload/example_data/count_mat.csv',
     '/path/to/server/workspace/upload/example_data/metadata_2.csv',
     '/path/to/server/workspace/upload/example_data/metadata.csv',
     '/path/to/server/workspace/upload/example_data/recipes.csv']


**List files and directory in cloud_storage**


```python
connector.listdir_cloud_storage()
```


    ['bioturing-lens', 'bioturingdebug', 'bioturingdebug.log.txt']


**Upload a single file**


```python
connector.upload_file('path/to/local/count_mat.csv', server_folder_name='test', debug_mode=True)
```


    {'status': 0,
     'path': '/path/to/server/workspace/upload/test/v1.count_mat.csv',
     'url_path': '/path/to/server/workspace/upload/test/v1.count_mat.csv'}


**Upload a folder**


```python
connector.upload_folder('tsv_sample/', debug_mode=True)
```

      0%|          | 0.00/16.1M [00:00<?, ?B/s]

    Upload tsv_sample/matrix_200.csv.gz, chunk index : 1 ...


    100%|██████████| 16.1M/16.1M [00:29<00:00, 538kB/s]



    {'folder_name': 'tsv_sample',
     'file_path': ['tsv_sample/recipes.csv',
      'tsv_sample/SRP092402.tsv',
      'tsv_sample/matrix_200.csv.gz'],
     'server_path': ['/path/to/server/workspace/upload/tsv_sample/v1.recipes.csv',
      '/path/to/server/workspace/upload/tsv_sample/v1.SRP092402.tsv',
      '/path/to/server/workspace/upload/tsv_sample/v1.matrix_200.csv.gz']}


**Create new BulkRNAseq project from the uploaded folder path in the SmartBulk Server**


```python
submit_result = connector.create_project(
    group_id='personal',
    species='human',
    project_name='human sample',
    matrix_paths=['/path/to/server/workspace/upload/tsv_sample/v1.matrix_200.csv.gz'],
    metadata_paths=['/path/to/server/workspace/upload/tsv_sample/v1.SRP092402.tsv'],
    dataset_name='Sample Dataset',
    use_gene_symbols=True,
)
```

**Check project creation status**


```python
connector.check_project_status(submit_result=submit_result)
```

**Add new BulkRNAseq dataset to a project**


```python
submit_result = connector.add_project(
    project_id='prj_8dfbc6a8-4e22-444f-b4a2-4df000c48141',
    group_id='personal',
    species='human',
    matrix_paths=['/path/to/server/workspace//upload/tsv_sample/matrix_200.csv.gz'],
    metadata_paths=['/path/to/server/workspace//upload/tsv_sample/SRP092402.tsv'],
    dataset_name='Another Dataset',
    use_gene_symbols=True,
)
if submit_result:
    connector.check_project_status(submit_result=submit_result)
```

**Create new NanoString project from the uploaded folder path in the SmartBulk Server**
```python
# metadata is optional in Nanostring
submit_result = connector.create_project(
    group_id='personal',
    species='human',
    project_name='nanostring',
    dataset_name='RCC',
    rcc_folder_path='/path/to/server/workspace//upload/GSE268196_RCC/',
    aggregate_count=True,
    platform='bulk',
)
if submit_result:
    connector.check_project_status(submit_result=submit_result)
```

**Add new Nanostring dataset to a project**

Note that Nanostring accepts only one metadata file when creating a new project.

```python
# metadata is optional in Nanostring
submit_result = connector.add_project(
    group_id='personal',
    species='human',
    project_id='prj_566b623a-cdab-11ef-859d-48ad9afa0555',
    dataset_name='nanostring_2',
    rcc_folder_path='/path/to/server/workspace//upload/GSE268196_RCC/',
    metadata_paths=['/path/to/server/workspace//upload/RCC_matrix_file/metadata.tsv.gz'],
    aggregate_count=True,
    platform='nanostring',
)
if submit_result:
    connector.check_project_status(submit_result=submit_result)
```

**Add new Nanostring dataset from uploaded matrix and metadata to a project**

Note that Nanostring accepts only one matrix and one metadata file when creating a new project.

```python
submit_result = connector.add_project(
    group_id='personal',
    species='human',
    project_id='prj_566b623a-cdab-11ef-859d-48ad9afa0555',
    dataset_name='uploaded_matrix',
    matrix_paths=['/path/to/server/workspace//upload/RCC_matrix_file/matrix.tsv.gz'],
    metadata_paths=['/path/to/server/workspace//upload/RCC_matrix_file/metadata.tsv.gz'],
    aggregate_count=True,
    platform='nanostring',
)
if submit_result:
    connector.check_project_status(submit_result=submit_result)
```

**Create project with multiple datasets with a recipes file**

Create a new project with multiple dataset using recipes

    This recipes file is a csv file that includes: 

        dataset_name: the name of dataset
        path_on_server: server path to the file in one dataset
        file_type: can be matrix or metadata or rcc, identify the path_on_server type
        species: can be human, mouse, rat or monkey
        platform: can be bulk or nanostring

Sample recipes.csv file:

| dataset_name | path_on_server                                                                                                              | file_type | species | platform |
|--------------|-----------------------------------------------------------------------------------------------------------------------------|-----------|---------|---------|
| Dataset_1    | /path/to/server/workspace//upload/example_data/count_mat.csv | matrix    | human   | bulk |
| Dataset_1    | /path/to/server/workspace//upload/example_data/metadata.csv   | metadata  | human   | bulk |
| Dataset_2    | /path/to/server/workspace//upload/example_data/count_mat_2.csv | matrix    | human   | bulk |
| Dataset_2    | /path/to/server/workspace//upload/example_data/count_mat_3.csv | matrix    | human   | bulk |
| Dataset_2    | /path/to/server/workspace//upload/example_data/metadata_2.csv   | metadata  | human   | bulk |
| Dataset_2    | /path/to/server/workspace//upload/example_data/metadata_3.csv | metadata  | human   | bulk |
| Dataset_3    | /path/to/server/workspace//upload/example_data/metadata_3.csv | rcc  | human   | nanostring |



```python
connector.create_project_from_recipes(
    group_id='personal', 
    recipes_path='example_data/recipes.csv', 
    project_name='sample dataset',,
    aggregate_count=True, # Parameter for nanostring
    use_gene_symbols=True, # Parameter for bulkRNAseq
)
```

**Add new dataset to a project with a recipes file**


```python
connector.add_project_from_recipes(
    project_id='prj_8dfbc6a8-4e22-444f-b4a2-4df000c48141',
    group_id='personal', 
    recipes_path='data/recipes.csv',,
    aggregate_count=True, # Parameter for nanostring
    use_gene_symbols=True, # Parameter for bulkRNAseq
)
```

**Resume add dataset to a project with a recipes file using tracelog**


```python
connector.create_project_from_recipes(
    group_id='personal',
    recipes_path='data/recipes.csv', 
    project_name='21_bulk_datasets',
    trace_log='prj_8dfbc6a8-4e22-444f-b4a2-4df000c48141/project_trace_log.json',
    aggregate_count=True, # Parameter for nanostring
    use_gene_symbols=True, # Parameter for bulkRNAseq
)
```

or

```python
connector.add_project_from_recipes(
    project_id='prj_8dfbc6a8-4e22-444f-b4a2-4df000c48141',
    group_id='personal', 
    recipes_path='data/recipes.csv',
    trace_log='prj_8dfbc6a8-4e22-444f-b4a2-4df000c48141/project_trace_log.json',,
    aggregate_count=True, # Parameter for nanostring
    use_gene_symbols=True, # Parameter for bulkRNAseq
)
```