from financial_dataset_loader import load_market


MAPPING_SECTOR = {
    'NAME': 'name',
    'NAME_KOREAN': 'name_kr',
    'GICS_SECTOR_NAME': 'sector',
    'ticker_bbg_index': 'market_index'
}

DATA_SOURCE = 's3'

def open_ks_market():
    market = load_market(market_name='ks', option_data_source=DATA_SOURCE)
    market = market.rename(columns=MAPPING_SECTOR)
    return market
