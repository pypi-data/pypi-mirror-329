from .path_director import file_folder
from .dart_consts import MAPPING_REPORT_TYPE, MAPPING_CORP_CLASS, MAPPING_REMARK
from .dart_exceptions import KEYWORDS_TO_EXCLUDE, DATA_EXCEPTIONS
from .dart_connector import set_params_disclosure_list, fetch_response_disclosure_list, fetch_response_disclosure, set_params_disclosure, fetch_all_responses_disclosures_of_date
from .corpcode_utils import save_stock_corpcodes_of_menu2205, load_stock_corpcodes_of_menu2205, get_holdings_stock_corpcodes, get_holdings_bond_corpcodes, get_holdings_corpcodes
from .response_parser import get_list
from .xml_utils import unzip_xml, load_xml_as_root, load_as_text_and_save_cleaned_xml
from shining_pebbles import get_today, scan_files_including_regex, open_df_in_file_folder_by_regex, get_date_n_days_ago
from canonical_transformer import map_df_to_data, map_df_to_csv
from datetime import datetime, timedelta
from tqdm import tqdm
import pandas as pd
import requests
import zipfile
from io import BytesIO
import xml.etree.ElementTree as ET
from lxml import etree


def get_disclosure_list(corpcode, start_date=None, end_date=None, category=None, detailed_category=None, output='df'):
    end_date = (end_date or get_today()).replace('-', '')
    start_date = start_date or (datetime.strptime(end_date, '%Y%m%d') - timedelta(days=365)).strftime('%Y%m%d')
    params_disclosure = set_params_disclosure_list(corpcode=corpcode, start_date=start_date, end_date=end_date, category=category, detailed_category=detailed_category)
    response = fetch_response_disclosure_list(params_disclosure)
    disclosures = get_list(response)

    mapping_output = {
        'df': lambda x: pd.DataFrame(x).set_index('rcept_no'),
        'dataframe': lambda x: pd.DataFrame(x).set_index('rcept_no'),
        'json': lambda x: x,
        'dict': lambda x: x,
        'dct': lambda x: x,
    }

    if output not in mapping_output:
        raise ValueError(f"Invalid output type: {output}. Choose from {list(mapping_output.keys())}.")

    return mapping_output[output](disclosures)


def get_report_list(corpcode, start_date=None, end_date=None, category='quarter', output='df'):
    reports = get_disclosure_list(corpcode, start_date=start_date, end_date=end_date, category='A', detailed_category=category, output=output)
    return reports

def preprocess_disclosure_list(df, category=None):
    df['corp_code'] = df['corp_code'].map(lambda x: str(x).zfill(8))
    df['receipt_number'] = df['rcept_no']
    df['classification'] = df['corp_cls'].map(MAPPING_CORP_CLASS)
    df['ticker_bbg'] = df['stock_code'].map(lambda x: f"{str(x).zfill(6)} KS Equity")
    df['disclosure_title'] = df['report_nm'].str.strip()
    df['filer_name'] = df['flr_nm']
    df['receipt_date'] = df['rcept_dt'].astype(str).apply(lambda x: f'{x[:4]}-{x[4:6]}-{x[6:]}')
    df['remark'] = df['rm'].map(lambda x: MAPPING_REMARK.get(x, '-'))
    df['url'] = df['receipt_number'].map(get_dart_disclosure_url)
    cols_to_keep = ['receipt_number', 'corp_code', 'corp_name', 'classification', 'ticker_bbg', 'disclosure_title', 'filer_name', 'receipt_date', 'remark', 'url']
    if category is not None:
        df['category'] = category 
        cols_to_keep = cols_to_keep + ['category']
    df = df[cols_to_keep].set_index('receipt_number')
    return df


def get_full_disclosure_list(corpcode, start_date=None, end_date=None, preprocess=False):
    dfs = []
    for category in MAPPING_REPORT_TYPE.values():
        try:
            df = get_disclosure_list(corpcode, start_date=start_date, end_date=end_date, category=category, output='df')
            if preprocess:
                df = preprocess_disclosure_list(df=df, category=category)
            dfs.append(df)
        except Exception as e:
            print(f'No data for category:', category, e)
    df = pd.concat(dfs, axis=0).sort_index(ascending=False)
    return df

def get_preprocessed_full_disclosure_list(corpcode, start_date=None, end_date=None):
    df = get_full_disclosure_list(corpcode, start_date=start_date, end_date=end_date, preprocess=True)
    return df

def get_preprocessed_disclosure_list(corpcode, start_date=None, end_date=None, category='A'):
    df = get_disclosure_list(corpcode, start_date=start_date, end_date=end_date, category=category, output='df')
    df = preprocess_disclosure_list(df, category)
    return df

def save_report_xml(report_info):
    response = fetch_response_disclosure(set_params_disclosure(rcept_no=report_info.rcept_no))
    zip_content = response.content
    # file_name = f'xml-report-code{report_info.corp_code}-no{report_info.rcept_no}-at{report_info.rcept_dt}-save{get_today().replace("-","")}.xml'
    file_name = f'xml-report-code{report_info.corp_code}-no{report_info.rcept_no}-at{report_info.rcept_dt}.xml'
    report_xml = unzip_xml(zip_content, file_name=file_name)
    return report_xml

def load_report_as_root(report_info):
    report_xml = save_report_xml(report_info)
    file_name = f'xml-report-code{report_info.corp_code}-no{report_info.rcept_no}-at{report_info.rcept_dt}.xml'
    root = load_xml_as_root(file_name=file_name)
    return root

def save_clean_and_load_as_root(report_info):
    save_report_xml(report_info)
    file_name = f'xml-report-code{report_info.corp_code}-no{report_info.rcept_no}-at{report_info.rcept_dt}.xml'
    load_as_text_and_save_cleaned_xml(file_name=file_name)
    root = load_xml_as_root(file_name=file_name)
    return root

def fetch_and_load_xml_as_root(report_info):
    """
    Fetches the disclosure response, unzips the XML, and returns the XML root without saving files.

    Args:
        report_info: An object containing `rcept_no`, `corp_code`, `rcept_dt`.

    Returns:
        ElementTree.Element: The root of the XML document.
    """
    # Step 1: Fetch the API response
    response = fetch_response_disclosure(set_params_disclosure(rcept_no=report_info.rcept_no))
    zip_content = response.content

    try:
        # Step 2: Extract XML content from the zip file in memory
        zip_data = BytesIO(zip_content)
        with zipfile.ZipFile(zip_data) as zip_file:
            for filename in zip_file.namelist():
                content_xml = zip_file.read(filename).decode('utf-8')
                break  # Assume the first file in the zip is the desired XML

        # Step 3: Parse the XML content
        try:
            # Attempt to parse with ElementTree
            root = ET.ElementTree(ET.fromstring(content_xml)).getroot()
            return root
        except ET.ParseError:
            # If parsing fails, use lxml for recovery
            parser = etree.XMLParser(recover=True)
            tree = etree.fromstring(content_xml.encode('utf-8'), parser)
            cleaned_xml = etree.tostring(tree, encoding='utf-8', pretty_print=True).decode('utf-8')
            root = ET.ElementTree(ET.fromstring(cleaned_xml)).getroot()
            print("XML successfully cleaned and loaded.")
            return root

    except Exception as e:
        print(f"Error processing the zip or XML content: {e}")
        return None

def get_dart_disclosure_url(rcept_no):
    base_url = "https://dart.fss.or.kr/dsaf001/main.do"
    url = f"{base_url}?rcpNo={rcept_no}"
    return url

def get_disclosure_data(corpcode, start_date=None, end_date=None, category=None, detailed_category=None):
    df = get_disclosure_list(corpcode, start_date=start_date, end_date=end_date, category=category, detailed_category=detailed_category, output='df')
    df['url'] = df.index.map(get_dart_disclosure_url)
    data = map_df_to_data(df)
    return data


def get_data_disclosure_of_corps_in_menu2205(df, date_ref):
    start_date, end_date = date_ref, date_ref
    dct_disclosure = {}
    for index, row in tqdm(df[['name', 'corpcode']].iterrows()):
        name, corpcode = row
        try:
            disclosure = get_full_disclosure_list(corpcode=corpcode, start_date=start_date, end_date=end_date)
            dct_disclosure[name] = disclosure
        except:
            
            dct_disclosure[name] = None
    return dct_disclosure

def get_df_disclosures_of_corps_in_menu2205(df, date_ref):
    dct_disclosure = get_data_disclosure_of_corps_in_menu2205(df, date_ref)
    dfs = [df for df in dct_disclosure.values() if df is not None]
    df = pd.concat(dfs, axis=0)
    return df

def save_disclosures_of_corps_in_menu2205(df, date_ref=None):
    date_ref = date_ref or get_today()
    df = get_df_disclosures_of_corps_in_menu2205(df=df, date_ref=date_ref)
    file_name = f'dataset-holdings_disclosures-at{date_ref.replace("-", "")}-version{get_today("%Y%m%d%H%M").replace("-","")}-save{get_today().replace("-","")}.csv'
    map_df_to_csv(df=df, file_folder=file_folder['list'], file_name=file_name, include_index=True)
    return df

def open_df_disclosures_of_corps_in_menu2205(date_ref=None):
    date_ref = date_ref or get_today()
    regex = f'dataset-holdings_disclosures-at{date_ref.replace("-", "")}' if date_ref else 'dataset-holdings_disclosures-at'
    file_names = scan_files_including_regex(file_folder=file_folder['list'], regex=regex)
    df = open_df_in_file_folder_by_regex(file_folder=file_folder['list'], regex=file_names[-1]).reset_index()
    return df

load_disclosures_of_date = open_df_disclosures_of_corps_in_menu2205

def save_disclosures_of_date(date_ref=None):
    try:
        save_stock_corpcodes_of_menu2205(date_ref=date_ref)
        date_ref_menu2205 = date_ref
    except:
        print(f'Error saving corpcode of menu2205 on: {date_ref}.')
        date_ref_menu2205 = get_date_n_days_ago(date_ref, 1)
    df_corpcodes = load_stock_corpcodes_of_menu2205(date_ref=date_ref_menu2205)
    save_disclosures_of_corps_in_menu2205(df_corpcodes, date_ref=date_ref)
    df = open_df_disclosures_of_corps_in_menu2205(date_ref=date_ref)
    return df

def preprocess_df_disclosures_by_date(date_ref=None, keywords_to_exclude=KEYWORDS_TO_EXCLUDE):
    df = preprocess_disclosure_list(open_df_disclosures_of_corps_in_menu2205(date_ref=date_ref))
    df = df[~df['disclosure_title'].str.contains('|'.join(keywords_to_exclude))]
    return df

get_preprocessed_df_disclosures_of_date = preprocess_df_disclosures_by_date

def get_collection_of_data_disclosures_by_date(date_ref=get_today().replace("-", "")):
    responses = fetch_all_responses_disclosures_of_date(date_ref)
    collection_of_data = [response.json()['list'] for response in responses]
    return collection_of_data

def get_data_all_disclosures_by_date(date_ref=get_today().replace("-", "")):
    collection_of_data = get_collection_of_data_disclosures_by_date(date_ref)
    data = [item for data in collection_of_data for item in data]
    return data

def get_df_holding_disclosures_by_date(date_ref=get_today().replace("-", "")):
    data = get_data_all_disclosures_by_date(date_ref)
    df = pd.DataFrame(data)
    corpcodes_holding = get_holdings_corpcodes(date_ref=date_ref)
    df = df[df['corp_code'].isin(corpcodes_holding)]
    return df

def get_preprocessed_holdings_disclosures_by_date(date_ref=get_today().replace("-", ""), keywords_to_exclude=KEYWORDS_TO_EXCLUDE):
    df = get_df_holding_disclosures_by_date(date_ref)
    df = preprocess_disclosure_list(df)
    df = df[~df['disclosure_title'].str.contains('|'.join(keywords_to_exclude))]
    for exception in DATA_EXCEPTIONS:
        df = df[
            ~((df[exception['p']['key']].str.contains(exception['p']['value']))&(df[exception['q']['key']].str.contains(exception['q']['value'])))]
    return df
