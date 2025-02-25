from tqdm import tqdm
from dart_api_controller.disclosure_utils.disclosure_list_application import search_disclosures_including_keyword_by_date
from dart_api_controller.disclosure_utils.disclosure_list_utils import preprocess_disclosure_list
from shining_pebbles import extract_dates_ref_in_file_folder_by_regex, scan_files_including_regex, get_today
from canonical_transformer import map_csv_to_df, map_df_to_csv
from financial_dataset_preprocessor import ensure_n_digits_code
import pandas as pd
import os

def get_all_results_of_keyword(dates, keyword_title, keyword_content):
    dates_ref = extract_dates_ref_in_file_folder_by_regex(file_folder='dataset-result', regex=f'title{keyword_title}-content{keyword_content}-at.*')
    dfs = []
    for date in tqdm(dates[::-1]):
        if date not in dates_ref:
            print(f'|- search disclosures at {date}')
            try:
                df_including = search_disclosures_including_keyword_by_date(date_ref=date, keyword_title=keyword_title, keyword_content=keyword_content)
                dfs.append(df_including)
            except Exception as e:
                print(e)
                continue
    df = pd.concat(dfs)
    df = preprocess_disclosure_list(df)
    return df

def save_dart_search_results_of_keyword(keyword_title, keyword_content, date_save=None, option_save=True):
    regex = f'title{keyword_title}-content{keyword_content}-at.*'
    if date_save:
        regex = f'title{keyword_title}-content{keyword_content}-.*save{date_save.replace("-","")}'
    file_names = scan_files_including_regex(file_folder='dataset-result', regex=regex)
    dfs = []
    for file_name in file_names:
        df = map_csv_to_df(file_folder='dataset-result', file_name=file_name)
        df['stock_code'] = df['stock_code'].apply(lambda code: ensure_n_digits_code(corpcode=code, n=6))
        dfs.append(df)
    df = pd.concat(dfs)
    df = preprocess_disclosure_list(df)
    option_save = True
    if option_save:
        dates_ref = extract_dates_ref_in_file_folder_by_regex(file_folder='dataset-result', regex=f'title{keyword_title}-content{keyword_content}-at.*')
        start_date = dates_ref[0]
        end_date = dates_ref[-1]
        file_folder = 'dataset-result'
        file_name = f'dataset-dart_search_results-title{keyword_title}-content{keyword_content}-from{start_date.replace("-","")}-to{end_date.replace("-","")}-save{get_today().replace("-","")}.csv'
        file_path = os.path.join(file_folder, file_name)
        df.to_csv(file_path, encoding='utf-8-sig')
    return df