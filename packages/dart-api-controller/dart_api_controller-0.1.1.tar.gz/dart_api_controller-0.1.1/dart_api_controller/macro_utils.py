from shining_pebbles import get_date_range, get_today, scan_files_including_regex
from .path_director import file_folder
from .disclosure_utils import save_disclosures_of_date
from tqdm import tqdm

DATES_IN_RANGE = get_date_range(start_date_str='2021-07-21', end_date_str=get_today())[::-1]

def get_dates_existing(file_folder=file_folder['list']):
    file_names = scan_files_including_regex(file_folder=file_folder, regex='holdings_disclosures')
    dates_existing = [file_name.split('at')[-1].split('-')[0] for file_name in file_names]
    dates_existing_dashed = [f'{date[:4]}-{date[4:6]}-{date[6:]}' for date in dates_existing]
    return dates_existing_dashed

DATES_EXISTING = get_dates_existing()

def save_all_disclosures_of_date(dates_range=DATES_IN_RANGE):
    for date in tqdm(dates_range):
        if date not in DATES_EXISTING:
            try:
                save_disclosures_of_date(date_ref=date)
            except Exception as e:
                print(e)
                print(f'No disclosures on: {date}.')
    return None