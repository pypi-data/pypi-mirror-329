import os

def get_file_path(file_folder, file_name):
    return os.path.join(file_folder, file_name)


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
MODULE_DIR = os.path.join(ROOT_DIR)

DATA_DIR = './data-dart'
FILE_FOLDER_CORPCODE = 'data-corpcode'
FILE_FOLDER_DATASET_CORPCODE = 'dataset-corpcode'
FILE_FOLDER_REPORT = 'xml-report'
FILE_FOLDER_SECTOR = 'dataset-sector'
FILE_FOLDER_MARKET = 'dataset-market'
FILE_FOLDER_LIST = 'dataset-list'

file_folder = {
    'corpcode': get_file_path(DATA_DIR, FILE_FOLDER_CORPCODE),
    'dataset-corpcode': get_file_path(DATA_DIR, FILE_FOLDER_DATASET_CORPCODE),
    'report': get_file_path(DATA_DIR, FILE_FOLDER_REPORT),
    'sector': get_file_path(MODULE_DIR, FILE_FOLDER_SECTOR),
    'market': get_file_path(MODULE_DIR, FILE_FOLDER_MARKET),
    'list': get_file_path(DATA_DIR, FILE_FOLDER_LIST),
}