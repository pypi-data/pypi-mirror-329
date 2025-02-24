from .path_director import file_folder
import os
import re
import zipfile
from io import BytesIO
import xml.etree.ElementTree as ET
from lxml import etree


def unzip_xml(zip_content, file_name, file_folder=file_folder['report']):
    zip_data = BytesIO(zip_content)
    with zipfile.ZipFile(zip_data) as zip_file:
        print(zip_file.namelist())
        for filename in zip_file.namelist():
            content_xml = zip_file.read(filename).decode('utf-8')
            file_path = os.path.join(file_folder, file_name)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content_xml)
                print(f'|- {file_name} is saved.')
    return content_xml


def load_xml_as_root(file_name, file_folder=file_folder['report']):
    """
    XML 파일을 로드하고 문제가 있는 경우 clean 작업 후 반환

    Args:
        file_name (str): XML 파일 이름
        file_folder (str): XML 파일이 위치한 폴더 경로

    Returns:
        ElementTree.Element: XML 루트 요소
    """
    file_path = os.path.join(file_folder, file_name)
    
    try:
        # 시도 1: 기본 XML 파싱
        tree = ET.parse(file_path)
        return tree.getroot()
    except ET.ParseError as e:
        print(f"Initial parsing failed. Attempting to clean XML file: {e}")

        try:
            # lxml을 사용하여 XML 정리
            parser = etree.XMLParser(recover=True)
            with open(file_path, 'r', encoding='utf-8') as f:
                tree = etree.parse(f, parser)

            # 정리된 XML을 문자열로 변환 후 다시 ElementTree로 파싱
            cleaned_xml = etree.tostring(tree, encoding='utf-8', pretty_print=True).decode('utf-8')
            root = ET.ElementTree(ET.fromstring(cleaned_xml)).getroot()
            print("XML successfully cleaned and loaded.")
            return root
        except Exception as clean_error:
            print(f"Error cleaning XML file: {clean_error}")
            return None
    except Exception as e:
        print(f"Unexpected error loading XML file: {e}")
        return None


# import re
# from io import StringIO

# def clean_and_parse_xml(content):
#     """
#     Cleans invalid XML tokens (like '<>' in text) and parses the XML content.

#     Args:
#         content (str): Raw XML content as a string.

#     Returns:
#         ElementTree.Element: Cleaned XML root element.
#     """
#     try:
#         # Step 1: Replace invalid < and > in text content
#         cleaned_content = re.sub(r"<([^/a-zA-Z!?])", r"&lt;\1", content)  # Replace '<' not followed by valid tag names
#         cleaned_content = re.sub(r"([^a-zA-Z0-9!?])>", r"\1&gt;", cleaned_content)  # Replace '>' not preceded by valid tag names
        
#         # Step 2: Try parsing with ElementTree
#         root = ET.ElementTree(ET.fromstring(cleaned_content)).getroot()
#         return root
#     except ET.ParseError:
#         # Step 3: Use lxml to recover XML
#         parser = etree.XMLParser(recover=True)
#         root = etree.parse(StringIO(cleaned_content), parser).getroot()
#         print("XML was cleaned and recovered.")
#         return root
#     except Exception as e:
#         print(f"Error parsing XML: {e}")
#         return None

# def load_xml_as_root(file_name, file_folder=file_folder['report']):
#     """
#     XML 파일을 로드하고 문제가 있는 경우 clean 작업 후 반환

#     Args:
#         file_name (str): XML 파일 이름
#         file_folder (str): XML 파일이 위치한 폴더 경로

#     Returns:
#         ElementTree.Element: XML 루트 요소
#     """
#     file_path = os.path.join(file_folder, file_name)

#     try:
#         # 시도 1: 기본 XML 파싱
#         tree = ET.parse(file_path)
#         return tree.getroot()
#     except ET.ParseError as e:
#         print(f"Initial parsing failed. Attempting to clean XML file: {e}")

#         try:
#             # Step 2: lxml을 사용하여 XML 정리
#             parser = etree.XMLParser(recover=True)
#             with open(file_path, 'r', encoding='utf-8') as f:
#                 content = f.read()

#             # Step 3: clean_and_parse_xml 함수를 호출하여 비정상 토큰 정리 후 파싱
#             root = clean_and_parse_xml(content)
#             if root is not None:
#                 print("XML successfully cleaned using clean_and_parse_xml.")
#                 return root

#             # Fallback: lxml recover mode
#             tree = etree.parse(StringIO(content), parser)
#             cleaned_xml = etree.tostring(tree, encoding='utf-8', pretty_print=True).decode('utf-8')
#             root = ET.ElementTree(ET.fromstring(cleaned_xml)).getroot()
#             print("XML successfully cleaned and loaded using lxml fallback.")
#             return root

#         except Exception as clean_error:
#             print(f"Error cleaning XML file: {clean_error}")
#             return None
#     except Exception as e:
#         print(f"Unexpected error loading XML file: {e}")
#         return None



def load_xml_as_text(file_name, file_folder=file_folder['report']):
    """
    XML 파일을 문자열로 로드하는 함수

    Args:
        file_name (str): XML 파일 이름
        file_folder (str): XML 파일이 위치한 폴더 경로

    Returns:
        str: XML 파일 전체 내용을 문자열로 반환
    """
    file_path = os.path.join(file_folder, file_name)  # 파일 경로 결합
    print(f"Loading file: {file_path}")
    
    try:
        # 파일을 텍스트 모드로 열어서 읽기
        with open(file_path, 'r', encoding='utf-8') as file:
            xml_text = file.read()  # 파일 전체 내용을 읽어 문자열로 저장
        return xml_text  # 문자열 반환
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return ""
    except Exception as e:
        print(f"Error loading file: {e}")
        return ""


def save_cleaned_xml(xml_text, file_name, file_folder=file_folder['report'], suffix=False):
    """
    잘못된 <, > 사용을 수정하고 수정된 XML을 새 파일에 저장하는 함수.

    Args:
        xml_text (str): 원본 XML 문자열
        file_name (str): 원본 XML 파일 이름
        file_folder (str): XML 파일이 위치한 폴더 경로

    Returns:
        str: 저장된 파일의 경로
    """
    # Step 1: 잘못된 <와 >를 정규 표현식으로 치환 (한글 또는 숫자로 시작하는 경우만)
    cleaned_text = re.sub(r'<([가-힣\d][^<>]*)>', r'&lt;\1&gt;', xml_text)
    cleaned_text = cleaned_text.replace('R&D', 'R;D')  # Replace 'R&D' with 'R&amp;D'
    print("Invalid < and > replaced selectively.")

    # Step 2: 새로운 파일 이름 생성
    base_name, ext = os.path.splitext(file_name)
    new_file_name = f"{base_name}-cleaned.xml" if suffix else base_name
    new_file_path = os.path.join(file_folder, new_file_name)

    # Step 3: 수정된 문자열을 새 파일에 저장
    with open(new_file_path, 'w', encoding='utf-8') as file:
        file.write(cleaned_text)
        print(f"Cleaned XML saved to: {new_file_path}")

    return new_file_name


def load_as_text_and_save_cleaned_xml(file_name, file_folder=file_folder['report'], suffix=False):
    """
    XML 파일을 로드하고 잘못된 토큰을 수정하여 새 파일에 저장하는 함수.

    Args:
        file_name (str): XML 파일 이름
        file_folder (str): XML 파일이 위치한 폴더 경로

    Returns:
        str: 저장된 파일의 경로
    """
    xml_text = load_xml_as_text(file_name, file_folder)
    if not xml_text:
        return ""

    return save_cleaned_xml(xml_text, file_name, file_folder, suffix)


def xml_to_json(xml_string):
    """
    Convert an XML string to a JSON object.

    Parameters:
        xml_string (str): The XML string to convert.

    Returns:
        dict: The converted JSON object.
    """
    try:
        root = ET.fromstring(xml_string)
        result = []

        for list_elem in root.findall("list"):
            entry = {child.tag: child.text.strip() if child.text else None for child in list_elem}
            result.append(entry)

        return result
    except ET.ParseError as e:
        print(f"Error parsing XML: {e}")
        return None
