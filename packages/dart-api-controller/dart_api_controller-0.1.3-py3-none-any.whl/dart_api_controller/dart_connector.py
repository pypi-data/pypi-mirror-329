import requests
from .dart_consts import DART_API_KEY, DART_API_CORPCODE_URL, DART_API_DISCLOSURE_LIST_URL, DART_API_DISCLOSURE_URL, PARAMS_DEFAULT, MAPPING_REPORT_TYPE, MAPPING_DETAILED_REPORT_TYPE
from shining_pebbles import get_today
import certifi
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def fetch_api_response(url, params=PARAMS_DEFAULT):
    # session = requests.Session()
    # retry = Retry(connect=3, backoff_factor=0.5)
    # adapter = HTTPAdapter(max_retries=retry)
    # session.mount('http://', adapter)
    # session.mount('https://', adapter)
    # response = session.get(url, params=params, verify=False)
    response = requests.get(url, params=params, verify=False)

    return response

def fetch_response_corpcode():
    response = fetch_api_response(url=DART_API_CORPCODE_URL, params=PARAMS_DEFAULT)
    return response

def fetch_response_disclosure_list(params):
    response = fetch_api_response(url=DART_API_DISCLOSURE_LIST_URL, params=params)
    return response

def fetch_response_disclosure(params):
    response = fetch_api_response(url=DART_API_DISCLOSURE_URL, params=params)
    return response

def set_params_corpcode():
    params = {
        **PARAMS_DEFAULT,
    }
    return params

def set_params_report_list(corpcode, start_date, end_date, category, final=True):
    params = {
        'crtfc_key': DART_API_KEY,           
        'corp_code': corpcode,        
        'bgn_de': start_date.replace('-', ''),          
        'end_de': end_date.replace('-', ''),          
        'pblntf_ty': 'A',               
    }
    if category:
        params['pblntf_detail_ty'] = MAPPING_DETAILED_REPORT_TYPE.get(category, category)

    if final:
        params['last_reprt_at'] = 'Y'

    return params

def set_params_disclosure_list(corpcode, start_date, end_date, category=None, detailed_category=None, final=True):
    params = {
        'crtfc_key': DART_API_KEY,
        'corp_code': corpcode,
        'bgn_de': start_date.replace('-', ''),
        'end_de': end_date.replace('-', '')
    }
    if category:
        params['pblntf_ty'] = MAPPING_REPORT_TYPE.get(category, category)
    
    if detailed_category:
        params['pblntf_detail_ty'] = MAPPING_DETAILED_REPORT_TYPE.get(detailed_category, detailed_category)

    if final:
        params['last_reprt_at'] = 'Y'
    
    return params


def set_params_disclosure(rcept_no):
    params = {
        **PARAMS_DEFAULT,
        'rcept_no': rcept_no,
    }
    return params



def fetch_response_disclosures_on_page_of_date(date_ref=get_today(), page_no=1):
    date_ref = date_ref.replace("-", "")
    params = {
        'crtfc_key': DART_API_KEY,        # API 인증키
        'bgn_de': date_ref,             # 시작일
        'end_de': date_ref,             # 종료일
        'last_reprt_at': 'Y',        # 최종보고서만 검색
        'page_no': str(page_no),              # 페이지 번호
        'page_count': '100',         # 페이지당 건수 (최대 100)
    }
    response = fetch_response_disclosure_list(params)
    return response


def fetch_response_all_disclosures_of_date(date_ref=get_today(), page_no=1):
    date_ref = date_ref.replace("-", "")
    params = {
        'crtfc_key': DART_API_KEY,        # API 인증키
        'bgn_de': date_ref,             # 시작일
        'end_de': date_ref,             # 종료일
        'last_reprt_at': 'Y',        # 최종보고서만 검색
        'page_no': str(page_no),              # 페이지 번호
        'page_count': '100',         # 페이지당 건수 (최대 100)
    }
    response = fetch_response_disclosure_list(params)
    return response


def fetch_response_disclosures_on_page_of_date(date_ref=get_today(), page_no=1):
    date_ref = date_ref.replace("-", "")
    params = {
        'crtfc_key': DART_API_KEY,        # API 인증키
        'bgn_de': date_ref,             # 시작일
        'end_de': date_ref,             # 종료일
        'last_reprt_at': 'Y',        # 최종보고서만 검색
        'page_no': str(page_no),              # 페이지 번호
        'page_count': '100',         # 페이지당 건수 (최대 100)
    }
    response = fetch_response_disclosure_list(params)
    return response

def fetch_all_responses_disclosures_of_date(date_ref=get_today()):
    date_ref = date_ref.replace("-", "")
    response_first = fetch_response_disclosures_on_page_of_date(date_ref=date_ref, page_no=1)
    maxmum_page_no = response_first.json().get('total_page')
    responses = [response_first]
    for page_no in range(2, maxmum_page_no+1):
        response = fetch_response_disclosures_on_page_of_date(date_ref=date_ref, page_no=page_no)
        responses.append(response)
    return responses

