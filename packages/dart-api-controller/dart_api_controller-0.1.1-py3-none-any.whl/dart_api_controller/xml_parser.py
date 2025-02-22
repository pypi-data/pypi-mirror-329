import pandas as pd


def extract_tags_with_keyword(root, keyword, tag_name=""):
    """
    Extracts tags with the specified name and keyword from the XML document.

    Parameters:
        root (Element): The root element of the XML document.
        tag_name (str): The name of the tag to search for.
        keyword (str): The keyword to search within the tag's text or attributes.

    Returns:
        dict: A dictionary containing the tag name, keyword, and matching results.
    """
    result = []

    # Find all tags with the specified name
    for elem in root.findall(f".//{tag_name}"):
        # Check if the keyword is in the text or attributes
        if (elem.text and keyword in elem.text) or any(keyword in str(value) for value in elem.attrib.values()):
            # Append the tag and its data to the result list
            result.append((tag_name, {
                "text": elem.text.strip() if elem.text else None,
                "attributes": elem.attrib
            }))

    # Return the result as a dictionary
    return {
        "tag_name": tag_name,
        "keyword": keyword,
        "result": result
    }



def extract_tables_with_keyword(root, keyword):
    """
    Extract tables containing a specific keyword from an XML document.

    Parameters:
        root (Element): The root element of the XML document.
        keyword (str): The keyword to search for within table rows.

    Returns:
        list: A list of dictionaries, each representing a table containing the keyword.
    """
    results = []

    # Find all <TABLE> tags
    for table in root.findall(".//TABLE"):
        table_data = {
            "headers": [],
            "rows": []
        }
        found = False

        # Extract headers if present
        thead = table.find(".//THEAD")
        if thead is not None:
            headers = [th.text.strip() if th.text else "" for th in thead.findall(".//TH")]
            table_data["headers"] = headers

        # Extract rows
        tbody = table.find(".//TBODY")
        if tbody is not None:
            for tr in tbody.findall(".//TR"):
                row = [td.text.strip() if td.text else "" for td in tr.findall(".//TD")]
                # Check if the keyword is in this row
                if any(keyword in cell for cell in row):
                    found = True
                table_data["rows"].append(row)

        # Add the table to results if the keyword was found
        if found:
            results.append(table_data)
    data = {
        "keyword": keyword,
        "results": results
    }
    return data

def extract_detailed_tables_with_keyword(root, keyword):
    """
    Extract tables containing a specific keyword from an XML document, including nested <P> tags.

    Parameters:
        root (Element): The root element of the XML document.
        keyword (str): The keyword to search for within table cells.

    Returns:
        list: A list of dictionaries, each representing a table containing the keyword.
    """
    results = []

    # Find all <TABLE> tags
    for table in root.findall(".//TABLE"):
        table_data = {
            "headers": [],
            "rows": []
        }
        found = False

        # Extract headers if present
        thead = table.find(".//THEAD")
        if thead is not None:
            headers = []
            for th in thead.findall(".//TH"):
                if th.find(".//P") is not None:
                    headers.append(th.find(".//P").text.strip() if th.find(".//P").text else "")
                else:
                    headers.append(th.text.strip() if th.text else "")
            table_data["headers"] = headers

        # Extract rows
        tbody = table.find(".//TBODY")
        if tbody is not None:
            for tr in tbody.findall(".//TR"):
                row = []
                for td in tr.findall(".//TD") + tr.findall(".//TE"):
                    # Check for nested <P> tags
                    if td.find(".//P") is not None:
                        cell_text = td.find(".//P").text.strip() if td.find(".//P").text else ""
                    else:
                        cell_text = td.text.strip() if td.text else ""
                    row.append(cell_text)

                    # Check if the keyword is in this cell
                    if keyword in cell_text:
                        found = True

                table_data["rows"].append(row)

        # Add the table to results if the keyword was found
        if found:
            results.append(table_data)

    data = {
        "keyword": keyword,
        "results": results
    }
    return data

def map_extracted_table_data_to_df(data_rows_and_headers):
    headers = data_rows_and_headers['headers']
    rows = data_rows_and_headers['rows']
    df = pd.DataFrame(data=rows, columns=headers)
    return df

# def map_extracted_table_data_to_df(data_rows_and_headers):
#     """
#     Map extracted table data with headers and rows to a Pandas DataFrame.

#     Parameters:
#         data_rows_and_headers (dict): A dictionary with keys 'headers' and 'rows'.

#     Returns:
#         pd.DataFrame: A DataFrame created from the headers and rows.
#     """
#     headers = data_rows_and_headers.get('headers', [])
#     rows = data_rows_and_headers.get('rows', [])

#     try:
#         # Attempt to create a DataFrame
#         df = pd.DataFrame(data=rows, columns=headers)
#     except ValueError as e:
#         print(f"Error creating DataFrame: {e}")

#         # Handle cases where the number of columns in rows doesn't match headers
#         max_columns = len(headers)
#         normalized_rows = [row + [None] * (max_columns - len(row)) for row in rows]
#         df = pd.DataFrame(data=normalized_rows, columns=headers)
#         print("Rows have been normalized to match headers.")

#     return df
