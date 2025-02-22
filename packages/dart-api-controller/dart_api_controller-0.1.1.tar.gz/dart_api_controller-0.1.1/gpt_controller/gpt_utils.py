from .gpt_constants import KEYS_OF_CHAT_COMPLETION
from .gpt_connector import GPT_API_KEY, GPT_MODEL_DEFAULT, gpt_client_default
from .date_utils import get_current_datetime_string
import ast
import re


def extract_lst_from_content(content):
    lst_pattern = r"\[.*\]"
    str_lst = re.findall(lst_pattern, content, re.DOTALL)[0]
    lst = ast.literal_eval(str_lst)
    return lst


def extract_dct_from_content(content):
    list_pattern = r"\{.*\}"
    str_dct = re.findall(list_pattern, content, re.DOTALL)[0]
    if str_dct:
        dct = ast.literal_eval(str_dct)
    else:
        dct = {}
    return dct


# def extract_description_from_content(content):
#     list_pattern = r"```python\s*\[.*?\]\s*```"
#     description = re.sub(list_pattern, "", content, flags=re.DOTALL).strip()
#     return description


def extract_text_from_content(content):
    code_block_pattern = r"```python\s*[\s\S]*?```"
    text_without_code_blocks = re.sub(code_block_pattern, "", content).strip()
    return text_without_code_blocks


def create_data_message(tuples):
    data_message = [{"role": role, "content": content} for role, content in tuples]
    return data_message


def get_chat_completion_on_prompts(prompts, api_key=None, gpt_client=None, model=None):
    api_key = api_key or GPT_API_KEY
    gpt_client = gpt_client or gpt_client_default
    model = model or GPT_MODEL_DEFAULT

    completion = gpt_client.chat.completions.create(
        model= model,
        messages=[
            {"role": "system", "content": f"Now you take on the role of an excellent AI assistant."},
            {"role": "user", "content": f"{prompts}"}
        ]
        )
    chat_completion = completion.choices[0].message
    return chat_completion

def generate_chat_completion_of_data_prompt(data_prompt, api_key=None, gpt_client=None, model=None):
    api_key = api_key or GPT_API_KEY
    gpt_client = gpt_client or gpt_client_default
    model = model or GPT_MODEL_DEFAULT

    completion = gpt_client.chat.completions.create(
        model= model,
        messages=data_prompt
        )
    chat_completion = completion.choices[0].message
    return chat_completion

def set_data_prompt(prompt_role, prompt_main, prompts_aux=None, prompt_format=None):
    data_messages=[
        {"role": "system", "content": f"{prompt_role}"},
        {"role": "user", "content": f"{prompt_main}"}
    ]
    if prompts_aux:
        for content in prompts_aux:
            data_messages.append({"role": "user", "content": f"{content}"})
    if prompt_format:
        data_messages.append({"role": "system", "content": f"{prompt_format}"})
    return data_messages

def get_data_from_response(response):
    keys_to_include = KEYS_OF_CHAT_COMPLETION
    dct_response = {key: getattr(response, key) for key in dir(response) if key in keys_to_include and not key.startswith('__') and not callable(getattr(response, key))}
    return dct_response

def get_data_in_chat_completion(datetime, data_prompt, data_response):
    dct = {}
    dct['datetime_messages'] = datetime
    dct['data_messages'] = data_prompt
    dct['datetime_response'] = get_current_datetime_string()
    dct['data_response'] = data_response
    return dct

def generate_metric_string_markdown(metrics):
    result = "```python\n{\n"
    for metric in metrics:
        result += f"    '{metric}': (min_{metric}, max_{metric}),\n"
    result += "}\n```"
    return result

# def extract_python_dict_from_string(input_string):
#     start_idx = input_string.find("```python") + len("```python\n")
#     end_idx = input_string.find("```", start_idx)
    
#     python_code = input_string[start_idx:end_idx].strip()    
#     python_dict = ast.literal_eval(python_code)
    
#     return python_dict

# def extract_python_list_from_string(input_string):
#     start_idx = input_string.find("```python") + len("```python\n")
#     end_idx = input_string.find("```", start_idx)
    
#     python_code = input_string[start_idx:end_idx].strip()    
#     python_list = ast.literal_eval(python_code)
    
#     return python_list