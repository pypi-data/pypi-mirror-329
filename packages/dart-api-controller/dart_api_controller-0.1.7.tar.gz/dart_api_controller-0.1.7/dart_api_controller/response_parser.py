import json

def get_content(response):
    return response.content

def parse_response(response):
    content = get_content(response)
    response = json.loads(content.decode('utf-8'))
    return response

def get_list(response):
    content = parse_response(response)
    lst = content['list']
    return lst

def get_message(response):
    content = parse_response(response)
    return content['message']

def get_status(response):
    content = parse_response(response)
    return content['status']

def get_page_no(response):
    content = parse_response(response)
    return content['page_no']

def get_page_count(response):
    content = parse_response(response)
    return content['page_count']

def get_limit(response):
    content = parse_response(response)
    return content['limit']

def get_current_page(response):
    content = parse_response(response)
    return content['current_page']

def get_total_page(response):
    content = parse_response(response)
    return content['total_page']

def get_total_count(response):
    content = parse_response(response)
    return content['total_count']


