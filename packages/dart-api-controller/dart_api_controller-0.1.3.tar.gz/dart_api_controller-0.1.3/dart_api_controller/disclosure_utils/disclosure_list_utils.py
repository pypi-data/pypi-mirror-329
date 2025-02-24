# from .path_director import file_folder
# from .dart_connector import set_params_disclosure_list, fetch_response_disclosure_list, fetch_response_disclosure, set_params_disclosure, fetch_all_responses_disclosures_of_date
# from .corpcode_utils import save_stock_corpcodes_of_menu2205, load_stock_corpcodes_of_menu2205, get_holdings_stock_corpcodes, get_holdings_bond_corpcodes, get_holdings_corpcodes
# from .response_parser import get_list
# from .xml_utils import unzip_xml, load_xml_as_root, load_as_text_and_save_cleaned_xml
from shining_pebbles import get_today
# from tqdm import tqdm
import pandas as pd
# import requests
# import zipfile
# import xml.etree.ElementTree as ET

from .disclosure_list_fetcher import get_data_all_disclosures_by_date
from .disclosure_exceptions import KEYWORDS_TO_EXCLUDE, DATA_EXCEPTIONS
from dart_api_controller.dart_consts import MAPPING_CORP_CLASS, MAPPING_REMARK
from dart_api_controller.corpcode_utils import get_holdings_corpcodes

def get_df_holding_disclosures_by_date(date_ref=get_today().replace("-", "")):
    data = get_data_all_disclosures_by_date(date_ref)
    df = pd.DataFrame(data)
    corpcodes_holding = get_holdings_corpcodes(date_ref=date_ref)
    df = df[df['corp_code'].isin(corpcodes_holding)]
    return df

def get_dart_disclosure_url(rcept_no):
    base_url = "https://dart.fss.or.kr/dsaf001/main.do"
    url = f"{base_url}?rcpNo={rcept_no}"
    return url

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

def get_preprocessed_holdings_disclosures_by_date(date_ref=get_today().replace("-", ""), keywords_to_exclude=KEYWORDS_TO_EXCLUDE):
    df = get_df_holding_disclosures_by_date(date_ref)
    df = preprocess_disclosure_list(df)
    pattern = '|'.join(keywords_to_exclude)
    df = df[~df['disclosure_title'].str.contains(pattern, regex=True)]
    for exception in DATA_EXCEPTIONS:
        df = df[
            ~((df[exception['p']['key']].str.contains(exception['p']['value']))&(df[exception['q']['key']].str.contains(exception['q']['value'])))]
    return df
