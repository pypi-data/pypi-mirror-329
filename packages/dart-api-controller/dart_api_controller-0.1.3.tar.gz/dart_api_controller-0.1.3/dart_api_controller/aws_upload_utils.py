from dart_api_controller import *
from shining_pebbles import *
from canonical_transformer import *
from aws_s3_controller import *

def scan_datasets_corpcode_local(keyword):
    file_names_local = scan_files_including_regex(file_folder=file_folder['dataset-corpcode'], regex=f'{keyword}')
    return file_names_local

def scan_datasets_corpcode_aws(keyword):
    file_names_aws = scan_files_in_bucket_by_regex(bucket='dataset-rpa', bucket_prefix=f'dataset-dart_corpcode-{keyword}', regex=f'{keyword}', option='name')
    return file_names_aws

def scan_nonexsiting_file_names_in_aws(keyword):
    file_names_bond_local = scan_datasets_corpcode_local(keyword)
    file_names_bond_aws = scan_datasets_corpcode_aws(keyword)
    file_names_nonexisting = list(set(file_names_bond_local) - set(file_names_bond_aws))
    return file_names_nonexisting

def upload_nonexisting_corpcode_files_to_s3(keyword):
    file_names = scan_nonexsiting_file_names_in_aws(keyword=keyword)
    print(f'{len(file_names)} files to be uploaded.')
    for file_name in file_names:
        upload_files_to_s3(file_folder_local=file_folder['dataset-corpcode'], bucket='dataset-rpa', bucket_prefix=f'dataset-dart_corpcode-{keyword}', regex=file_name)
    return None

def upload_corpcode_file_to_s3(keyword, file_name):
    upload_files_to_s3(file_folder_local=file_folder['dataset-corpcode'], bucket='dataset-rpa', bucket_prefix=f'dataset-dart_corpcode-{keyword}', regex=file_name)
    return None

def upload_corpcode_stock_file_to_s3(file_name):
    upload_files_to_s3(file_folder_local=file_folder['dataset-corpcode'], bucket='dataset-rpa', bucket_prefix='dataset-dart_corpcode-stock', regex=file_name)
    return None

def upload_corpcode_bond_file_to_s3(file_name):
    upload_files_to_s3(file_folder_local=file_folder['dataset-corpcode'], bucket='dataset-rpa', bucket_prefix='dataset-dart_corpcode-bond', regex=file_name)
    return None

def upload_corpcode_file_to_s3(file_name):
    upload_files_to_s3(file_folder_local=file_folder['dataset-corpcode'], bucket='dataset-rpa', bucket_prefix='dataset-dart_corpcode', regex=file_name)
    return None