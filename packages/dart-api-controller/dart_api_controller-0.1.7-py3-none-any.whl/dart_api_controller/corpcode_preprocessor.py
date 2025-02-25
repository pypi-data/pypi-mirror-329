
import pandas as pd
def ensure_8digits_corpcode(corpcode):
    if pd.isna(corpcode):
        return None
    if isinstance(corpcode, float):
        corpcode = str(int(corpcode)).replace('.0', '').zfill(8)
    elif isinstance(corpcode, int):
        corpcode = str(corpcode).zfill(8)
    elif isinstance(corpcode, str):
        corpcode = corpcode.replace('.0', '').zfill(8)
    elif isinstance(corpcode, np.number):
        corpcode = str(int(corpcode)).replace('.0', '').zfill(8)
    return corpcode

format_corpcode = ensure_8digits_corpcode