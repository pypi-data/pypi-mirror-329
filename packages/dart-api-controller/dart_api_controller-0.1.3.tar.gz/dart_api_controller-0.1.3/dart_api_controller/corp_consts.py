from .dataset_loader import open_ks_market
from .corpcode_utils import load_corpcodes, load_listed_corpcodes

CORPCODES_KS = load_corpcodes()['corp_code'].tolist()
STOCKCODES_KS = load_listed_corpcodes()['stock_code'].tolist()
TICKERS_KS = open_ks_market().index.tolist()
