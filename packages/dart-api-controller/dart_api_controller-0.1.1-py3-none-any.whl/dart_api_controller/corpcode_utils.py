from .dart_consts import *
from .path_director import file_folder
from .dart_connector import *
from .corpcode_preprocessor import ensure_8digits_corpcode
from .aws_upload_utils import upload_corpcode_file_to_s3
from financial_dataset_preprocessor import get_df_stock_holdings_corpname, get_df_bond_holdings_corpname, get_df_holdings_corpname
import zipfile
import xml.etree.ElementTree as ET
import json
from tqdm import tqdm
from shining_pebbles import get_today, get_yesterday, scan_files_including_regex, open_df_in_file_folder_by_regex, open_json_in_file_folder_by_regex
from canonical_transformer import map_data_to_df, map_df_to_data, map_df_to_csv, map_df_to_some_data

def download_zip_corpcodes(file_name=None, file_folder=file_folder['corpcode']):
    file_name_zip = file_name or f'zip-corpcode-save{get_today().replace("-", "")}.zip'
    file_path_zip = os.path.join(file_folder, file_name_zip)
    response = fetch_response_corpcode()
    with open(file_path_zip, 'wb') as f:
        f.write(response.content)
    print(f'|- zip downloaded: {file_path_zip}')
    return file_name_zip

def unzip_corpcodes(file_name_zip=None, file_folder=file_folder['corpcode'], file_folder_extract=file_folder['corpcode']):
    file_name_zip = file_name_zip or f'zip-corpcode-save{get_today().replace("-", "")}.zip'
    file_path_zip = os.path.join(file_folder, file_name_zip)
    file_path_extract = os.path.join(file_folder_extract)
    file_name_extract = f'xml-corpcode-at{get_today().replace("-", "")}-save{get_today().replace("-", "")}.xml'
    with zipfile.ZipFile(file_path_zip, 'r') as zip_ref:
        zip_ref.extractall(file_path_extract)

    with zipfile.ZipFile(file_path_zip, 'r') as zip_ref:
        zip_ref.extractall(file_path_extract)
        original_file = os.path.join(file_path_extract, 'CORPCODE.xml')
        new_file = os.path.join(file_path_extract, file_name_extract)
        os.rename(original_file, new_file)

    print(f'|- zip extracted: {file_path_extract}')
    return file_name_extract


def map_xml_to_json(file_name_xml, file_folder=file_folder['corpcode']):
    file_path_xml = os.path.join(file_folder, file_name_xml)
    file_name_json = file_name_xml.replace('xml-', 'data-').replace('.xml', '.json')
    file_path_json = os.path.join(file_folder, file_name_json)
    tree = ET.parse(file_path_xml)
    root = tree.getroot()

    corps = []
    for corp in root.findall('.//list'):
        data_corp = {
            'corp_code': corp.findtext('corp_code'),
            'corp_name': corp.findtext('corp_name'),
            'stock_code': corp.findtext('stock_code').strip(),
            'modify_date': corp.findtext('modify_date')
        }
        corps.append(data_corp)

    with open(file_path_json, 'w', encoding='utf-8') as f:
        json.dump(corps, f, ensure_ascii=False, indent=2)
    
    print(f'|- json saved: {file_path_json}')
    return corps

def download_data_corpcodes(file_name=None, file_folder=file_folder['corpcode']):
    print('|- downloading corpcode data...')
    file_name_zip = download_zip_corpcodes(file_name, file_folder)
    file_name_xml = unzip_corpcodes(file_name_zip, file_folder)
    data = map_xml_to_json(file_name_xml, file_folder)
    print('|- corpcode data downloaded')
    return data

def load_data_corpcodes(file_name=None, date_ref=None, file_folder=file_folder['corpcode']):
    regex = 'data-corpcode-.*\.json'
    if date_ref:
        regex = f'data-corpcode-at{date_ref.replace("-", "")}.*\.json'
    file_names = scan_files_including_regex(file_folder=file_folder, regex=regex)
    file_name = file_names[-1]
    data = open_json_in_file_folder_by_regex(file_folder=file_folder, regex=file_name)
    print(f'|- corpcode data loaded: {file_name}')
    return data

def open_df_corpcodes(file_name=None, date_ref=None, file_folder=file_folder['corpcode']):
    data = load_data_corpcodes(file_name, date_ref, file_folder)
    df = map_data_to_df(data)
    print(f'|- corpcode data loaded to df: {df.shape}')
    return df

load_corpcodes = open_df_corpcodes

def open_df_listed_corpcodes(file_name=None, date_ref=None, file_folder=file_folder['corpcode']):
    df = load_corpcodes(file_name, date_ref, file_folder)
    df = df[df['stock_code'].str.len() > 0]
    print(f'|- listed corpcode data: {df.shape}')
    return df

load_listed_corpcodes = open_df_listed_corpcodes

def search_corpcode_data(corp_name, option='json'):
    df = load_corpcodes()
    result = df[df['corp_name'].str.contains(corp_name)]
    print(f'|- corpcode data: {result.shape}')
    if option in ['json', 'dict']:
        result = map_df_to_data(result)
    return result

def search_listed_corpcode_data(corp_name='', option='json'):
    df = load_corpcodes()
    result = df[(df['corp_name'].str.contains(corp_name))&(df['stock_code'].str.len() > 0)]
    print(f'|- listed corpcode data: {result.shape}')
    if option in ['json', 'dict']:
        result = map_df_to_data(result)
    return result

def get_corpcodes_including_name(corp_name, listed=False):
    data_corpcodes = search_corpcode_data(corp_name) if not listed else search_listed_corpcode_data(corp_name)
    print(f'corp codes related to {corp_name}:')
    corpcodes = []
    for datum in data_corpcodes:
        corp_name, stock_code, corp_code = datum['corp_name'], datum['stock_code'], datum['corp_code']
        stock_code = f'({stock_code})' if stock_code else None
        print(f'|- {corp_name} ({stock_code}): ({corp_code})')
        corpcodes.append(corp_code)
    return corpcodes

def get_corpcode_by_ticker(ticker):
    ticker = ticker[:6]
    df = load_corpcodes()
    corpname = df[df['stock_code'] == ticker].iloc[0]['corp_name']
    corpcode = df[df['stock_code'] == ticker].iloc[0]['corp_code']
    print(f'|- ticker {ticker} ... {corpname}({corpcode})')
    return corpcode

def get_corpcode_anyway(ticker, name, corpname, hotfix):
    try:
        corpcode = get_corpcode_by_ticker(ticker)
    except:
        print(f'|- ticker {ticker} not found')
        try:
            corpcode = get_corpcodes_including_name(corp_name=name)[-1]
        except:
            print(f'|- name {name} not found')
            try:
                corpcode = get_corpcodes_including_name(corp_name=corpname)[-1]
            except:
                print(f'|- corpname {corpname} not found')
                try:
                    corpcode = get_corpcodes_including_name(corp_name=hotfix)[-1]
                except:
                    print(f'|- corpcode not found')
                    corpcode = None
    return corpcode

def get_corpcode_anyway_without_ticker(name, corpname, hotfix):
    try:
        corpcode = get_corpcodes_including_name(corp_name=name)[-1]
    except:
        print(f'|- name {name} not found')
        try:
            corpcode = get_corpcodes_including_name(corp_name=corpname)[-1]
        except:
            print(f'|- corpname {corpname} not found')
            try:
                corpcode = get_corpcodes_including_name(corp_name=hotfix)[-1]
            except:
                print(f'|- corpcode not found')
                corpcode = None
    return corpcode


def get_data_corpcodes_in_menu2205(df_ticker_name_corpname):
    corpcodes = {}
    for _, row in tqdm(df_ticker_name_corpname.iterrows()):
        ticker, name, corpname, hotfix = row["ticker"], row["name"].split(' ')[0], row["corpname"], row["hotfix"]
        corpcode = get_corpcode_anyway(ticker, name, corpname, hotfix)
        corpcodes[ticker] = corpcode
    return corpcodes

def get_df_stock_corpcodes_of_menu2205(date_ref=None, exceptions=True):
    df = get_df_stock_holdings_corpname(date_ref=date_ref)
    df['corpcode'] = df.apply(lambda row: get_corpcode_anyway(row['종목코드'], row['종목명'], row['종목정보: 발행기관'], row['hotfix']), axis=1)
    return df

def save_stock_corpcodes_of_menu2205(date_ref=None, option_s3_upload=False):
    date_ref = get_yesterday() if date_ref is None else date_ref
    df = get_df_stock_corpcodes_of_menu2205(date_ref=date_ref)
    file_name = f'dataset-holdings_stock_corpcodes-code000000-at{date_ref.replace("-","")}-save{get_today().replace("-","")}.csv'
    map_df_to_csv(df, file_folder=file_folder['dataset-corpcode'], file_name=file_name)
    if option_s3_upload:
        print(f'🪣 saving stock corpcode to s3: {file_name}')
        upload_corpcode_file_to_s3(file_name=file_name)
    return df

def open_df_stock_corpcodes_of_menu2205(date_ref=None):
    regex = f'dataset-holdings_stock_corpcodes-code000000-at{date_ref.replace("-","")}-.*\.csv' if date_ref else 'dataset-holdings_stock_corpcodes-code000000-.*\.csv'
    file_name = scan_files_including_regex(file_folder=file_folder['dataset-corpcode'], regex=regex)[-1]
    df = open_df_in_file_folder_by_regex(file_folder=file_folder['dataset-corpcode'], regex=file_name).reset_index()
    df['corpcode'] = df['corpcode'].apply(ensure_8digits_corpcode)
    return df

load_stock_corpcodes_of_menu2205 = open_df_stock_corpcodes_of_menu2205

def get_holdings_stock_corpcodes(date_ref=None):
    try:
        df_corpcodes = load_stock_corpcodes_of_menu2205(date_ref=date_ref)
    except:
        print(f'|- corpcode data not found')
        print(f'|- saving corpcode data: {date_ref}')
        save_stock_corpcodes_of_menu2205(date_ref)
        print(f'|- load alternative corpcode data: latest')
        df_corpcodes = load_stock_corpcodes_of_menu2205()
    corpcodes_holding = df_corpcodes['corpcode'].tolist()
    return corpcodes_holding

def get_df_bond_corpcodes_of_menu2205(date_ref=None, exceptions=True):
    df = get_holdings_bond_corpcodes(date_ref=date_ref)
    df = df[df['종목명']!='국고채권']
    df['corpcode'] = df.apply(lambda row: get_corpcode_anyway(row['종목코드'], row['종목명'], row['종목정보: 발행기관'], row['hotfix']), axis=1)
    return df

def save_bond_corpcodes_of_menu2205(date_ref=None, option_s3_upload=False):
    date_ref = get_yesterday() if date_ref is None else date_ref
    df = get_df_bond_holdings_corpname(date_ref=date_ref)
    file_name = f'dataset-holdings_bond_corpcodes-code000000-at{date_ref.replace("-","")}-save{get_today().replace("-","")}.csv'
    map_df_to_csv(df, file_folder=file_folder['dataset-corpcode'], file_name=file_name)
    if option_s3_upload:
        print(f'🪣 saving bond corpcode to s3: {file_name}')
        upload_corpcode_file_to_s3(file_name=file_name)
    return df

def open_df_bond_corpcodes_of_menu2205(date_ref=None):
    regex = f'dataset-holdings_bond_corpcodes-code000000-at{date_ref.replace("-","")}-.*\.csv' if date_ref else 'dataset-holdings_bond_corpcodes-code000000-.*\.csv'
    file_name = scan_files_including_regex(file_folder=file_folder['dataset-corpcode'], regex=regex)[-1]
    df = open_df_in_file_folder_by_regex(file_folder=file_folder['dataset-corpcode'], regex=file_name).reset_index()
    df = df[df['종목명']!='국고채권']
    df['corpcode'] = df['corpcode'].apply(ensure_8digits_corpcode)
    return df

load_bond_corpcodes_of_menu2205 = open_df_bond_corpcodes_of_menu2205

def get_holdings_bond_corpcodes(date_ref=None):
    try:
        df_corpcodes = load_bond_corpcodes_of_menu2205(date_ref=date_ref)
    except:
        print(f'|- corpcode data not found')
        print(f'|- saving corpcode data: {date_ref}')
        save_bond_corpcodes_of_menu2205(date_ref)
        print(f'|- load alternative corpcode data: latest')
        df_corpcodes = load_bond_corpcodes_of_menu2205()
    corpcodes_holding = df_corpcodes['corpcode'].tolist()
    return corpcodes_holding

def get_corpcodes_of_menu2205(date_ref=None):
    df = get_df_holdings_corpname(date_ref=date_ref)
    df = df[df['종목명']!='국고채권']
    df['corpcode'] = df.apply(lambda row: get_corpcode_anyway(row['종목코드'], row['종목명'], row['종목정보: 발행기관'], row['hotfix']), axis=1)
    return df

def save_corpcodes_of_menu2205(date_ref=None, option_s3_upload=False):
    date_ref = get_yesterday() if date_ref is None else date_ref
    df = get_corpcodes_of_menu2205(date_ref=date_ref)
    file_name = f'dataset-holdings_corpcodes-code000000-at{date_ref.replace("-","")}-save{get_today().replace("-","")}.csv'
    map_df_to_csv(df, file_folder=file_folder['dataset-corpcode'], file_name=file_name)
    if option_s3_upload:
        print(f'🪣 saving corpcode to s3: {file_name}')
        upload_corpcode_file_to_s3(file_name=file_name)
    return df

def open_df_corpcodes_of_menu2205(date_ref=None):
    regex = f'dataset-holdings_corpcodes-code000000-at{date_ref.replace("-","")}-.*\.csv' if date_ref else 'dataset-holdings_corpcodes-code000000-.*\.csv'
    file_name = scan_files_including_regex(file_folder=file_folder['dataset-corpcode'], regex=regex)[-1]
    df = open_df_in_file_folder_by_regex(file_folder=file_folder['dataset-corpcode'], regex=file_name).reset_index()
    df = df[df['종목명']!='국고채권']
    df['corpcode'] = df['corpcode'].apply(ensure_8digits_corpcode)
    return df

load_corpcodes_of_menu2205 = open_df_corpcodes_of_menu2205

def get_holdings_corpcodes(date_ref=None):
    try:
        df_corpcodes = load_corpcodes_of_menu2205(date_ref=date_ref)
    except:
        print(f'|- corpcode data not found')
        print(f'|- saving corpcode data: {date_ref}')
        save_corpcodes_of_menu2205(date_ref)
        print(f'|- load alternative corpcode data: latest')
        df_corpcodes = load_corpcodes_of_menu2205()
    corpcodes_holding = df_corpcodes['corpcode'].tolist()
    return corpcodes_holding


def get_mapping_of_column_pairs(df, key_col, value_col):
    data = map_df_to_some_data(df=df, cols=[key_col, value_col])
    mapping = {datum[key_col]: datum[value_col] for datum in data}
    return mapping

def get_mapping_stock_name_to_corpcode(date_ref=None):
    df = load_stock_corpcodes_of_menu2205(date_ref=date_ref)
    mapping = get_mapping_of_column_pairs(df=df, key_col='종목명', value_col='corpcode')
    return mapping

def get_mapping_bond_name_to_corpcode(date_ref=None):
    df = load_bond_corpcodes_of_menu2205(date_ref=date_ref)
    mapping = get_mapping_of_column_pairs(df=df, key_col='종목명', value_col='corpcode')
    return mapping