from dart_api_controller.dart_connector import fetch_all_responses_disclosures_of_date
from shining_pebbles import get_today

def get_collection_of_data_disclosures_by_date(date_ref=None):
    date_ref = date_ref or get_today().replace("-", "")
    responses = fetch_all_responses_disclosures_of_date(date_ref)
    collection_of_data = [response.json()['list'] for response in responses]
    return collection_of_data

def get_data_all_disclosures_by_date(date_ref=None):
    date_ref = date_ref or get_today().replace("-", "")
    collection_of_data = get_collection_of_data_disclosures_by_date(date_ref)
    data = [item for data in collection_of_data for item in data]
    return data
