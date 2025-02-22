from .path_director import file_folder
from shining_pebbles import open_df_in_file_folder_by_regex
from financial_dataset_loader import load_market


MAPPING_SECTOR = {
    'NAME': 'name',
    'NAME_KOREAN': 'name_kr',
    'GICS_SECTOR_NAME': 'sector',
    'ticker_bbg_index': 'market_index'
}

def open_ks_market():
    market = load_market(market_name='ks')
    market = market.rename(columns=MAPPING_SECTOR)
    return market
