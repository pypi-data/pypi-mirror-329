
from ..dart_connector import fetch_response_disclosure, set_params_disclosure


def fetch_disclosure_content(rcept_no):
    response = fetch_response_disclosure(set_params_disclosure(rcept_no=rcept_no))
    return response
