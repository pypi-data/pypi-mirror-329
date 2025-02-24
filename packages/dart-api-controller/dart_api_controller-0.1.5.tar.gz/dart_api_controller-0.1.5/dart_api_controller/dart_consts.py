from dotenv import load_dotenv
import os 

load_dotenv()

DART_API_KEY = os.getenv('LAM_DART_API_KEY')
# DART_API_KEY = os.getenv('MY_DART_API_KEY')

DART_API_DISCLOSURE_LIST_URL = os.getenv('DART_API_DISCLOSURE_LIST_URL')
DART_API_CORPCODE_URL = os.getenv('DART_API_CORPCODE_URL')
DART_API_DISCLOSURE_URL = os.getenv('DART_API_DISCLOSURE_URL')

PARAMS_DEFAULT = {
    'crtfc_key': DART_API_KEY,
}

MAPPING_REPORT_TYPE = {
   '정기공시': 'A',
   '주요사항보고': 'B', 
   '발행공시': 'C',
   '지분공시': 'D',
   '기타공시': 'E',
   '외부감사관련': 'F',
   '펀드공시': 'G',
   '자산유동화': 'H',
   '거래소공시': 'I',
   '공정위공시': 'J'
}

MAPPING_DETAILED_REPORT_TYPE = {
        'annual': 'A001',
        'half': 'H1',
        'quarter': 'Q1',
}

MAPPING_CORP_CLASS = {
    'Y': '유가증권시장',
    'K': '코스닥시장',
    'N': '코넥스시장',
    'E': '기타법인'
}

MAPPING_REMARK = {
    '유': '유가증권시장본부 소관',
    '코': '코스닥시장본부 소관',
    '채': '채권상장법인 공시사항',
    '넥': '코넥스시장 소관',
    '공': '공정거래위원회 소관',
    '연': '연결재무제표 포함',
    '정': '정정신고 있음',
    '철': '철회(간주)된 보고서'
}

