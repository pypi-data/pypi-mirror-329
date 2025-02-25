import os
import zipfile
from io import BytesIO
import xml.etree.ElementTree as ET
from lxml import etree

from ..dart_connector import fetch_response_disclosure, set_params_disclosure
from ..xml_utils import unzip_xml, load_xml_as_root, load_as_text_and_save_cleaned_xml

def save_report_xml(report_info):
    response = fetch_response_disclosure(set_params_disclosure(rcept_no=report_info.rcept_no))
    zip_content = response.content
    # file_name = f'xml-report-code{report_info.corp_code}-no{report_info.rcept_no}-at{report_info.rcept_dt}-save{get_today().replace("-","")}.xml'
    file_name = f'xml-report-code{report_info.corp_code}-no{report_info.rcept_no}-at{report_info.rcept_dt}.xml'
    report_xml = unzip_xml(zip_content, file_name=file_name)
    return report_xml

def load_report_as_root(report_info):
    report_xml = save_report_xml(report_info)
    file_name = f'xml-report-code{report_info.corp_code}-no{report_info.rcept_no}-at{report_info.rcept_dt}.xml'
    root = load_xml_as_root(file_name=file_name)
    return root

def save_clean_and_load_as_root(report_info):
    save_report_xml(report_info)
    file_name = f'xml-report-code{report_info.corp_code}-no{report_info.rcept_no}-at{report_info.rcept_dt}.xml'
    load_as_text_and_save_cleaned_xml(file_name=file_name)
    root = load_xml_as_root(file_name=file_name)
    return root

def fetch_and_load_xml_as_root(report_info):
    """
    Fetches the disclosure response, unzips the XML, and returns the XML root without saving files.

    Args:
        report_info: An object containing `rcept_no`, `corp_code`, `rcept_dt`.

    Returns:
        ElementTree.Element: The root of the XML document.
    """
    # Step 1: Fetch the API response
    response = fetch_response_disclosure(set_params_disclosure(rcept_no=report_info.rcept_no))
    zip_content = response.content

    try:
        # Step 2: Extract XML content from the zip file in memory
        zip_data = BytesIO(zip_content)
        with zipfile.ZipFile(zip_data) as zip_file:
            for filename in zip_file.namelist():
                content_xml = zip_file.read(filename).decode('utf-8')
                break  # Assume the first file in the zip is the desired XML

        # Step 3: Parse the XML content
        try:
            # Attempt to parse with ElementTree
            root = ET.ElementTree(ET.fromstring(content_xml)).getroot()
            return root
        except ET.ParseError:
            # If parsing fails, use lxml for recovery
            parser = etree.XMLParser(recover=True)
            tree = etree.fromstring(content_xml.encode('utf-8'), parser)
            cleaned_xml = etree.tostring(tree, encoding='utf-8', pretty_print=True).decode('utf-8')
            root = ET.ElementTree(ET.fromstring(cleaned_xml)).getroot()
            print("XML successfully cleaned and loaded.")
            return root

    except Exception as e:
        print(f"Error processing the zip or XML content: {e}")
        return None
