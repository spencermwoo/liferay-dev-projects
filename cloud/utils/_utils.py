from _settings import *

import builtins
import json
import requests

def print_flush(*objects, sep='', end='\n', flush=False):
    return builtins.print(objects, sep, end, flush=True)

builtins.__print__ = print_flush

def write_file(filename, content, write=True):
    with open(filename,"w" if write else "a", encoding="UTF-8") as file:
        file.write(content)

def log(f):
    def print_log(*args, **kwargs):
        params = ', '.join([str(arg) for arg in args])
        print(f"Running : {f.__name__}({params})")
        # print(f"{f.__code__.co_varnames}")

        
        
        # cmd = f'{function}({params})'
        # print(f"{args}")

        ret = f(*args, **kwargs)
        print(f"\t {ret}")

        return ret

    return print_log

# def get_api(f):
#     def wrap_get(url, *args, **kwargs):
#           get_url(url, data)
#           return response

#      return wrap_get
#         ret = f(*args, **kwargs)

# // Utils

def create_session():
    s = requests.Session()
    s.auth = (LIFERAY_CLOUD_USERNAME, LIFERAY_CLOUD_PASSWORD)
    s.headers.update({"Content-Type": "application/json; charset=UTF-8"})

    return s

def get_url(url: str):
    response = requests.get(url, auth=(LIFERAY_CLOUD_USERNAME, LIFERAY_CLOUD_PASSWORD))

    return json.loads(response.text)

def patch_url(url: str, data: str):
    if data:
        response = requests.patch(url, data=data, auth=(LIFERAY_CLOUD_USERNAME, LIFERAY_CLOUD_PASSWORD))
    else:
        response = requests.patch(url, auth=(LIFERAY_CLOUD_USERNAME, LIFERAY_CLOUD_PASSWORD))

    return response
    # return json.loads(response.text)

def post_url(url: str, data: str):
    if data:
        response = requests.post(url, data=data, auth=(LIFERAY_CLOUD_USERNAME, LIFERAY_CLOUD_PASSWORD))
    else:
        response = requests.post(url, auth=(LIFERAY_CLOUD_USERNAME, LIFERAY_CLOUD_PASSWORD))

    return response

def map_to_str(non_str, lower: bool):
    if type(non_str) is bool and lower:
        return {False: "false", True: "true"}[non_str]

    if lower:
        return lower(str(non_str))
    else:
        return str(non_str)
