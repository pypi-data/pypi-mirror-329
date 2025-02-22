import base64
import json
import logging
import socket
import typing as T
from dataclasses import fields

import requests

from .data import Resp
from .exceptions import ErrorResponseException, ErrorResp


def contains_none(args) -> bool:
    return None in args


def assert_not_none(*args):
    if contains_none(args):
        raise ValueError("None arguments are not allowed in this function call.")


def get_free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(('127.0.0.1', 0))
        return sock.getsockname()[1]


def handle_response(resp: requests.Response, code_to_dto_class: T.Dict[int, T.Type[T.Any]]) -> Resp:
    if resp.text.strip() == '':
        # Empty response is treated like an empty JSON object
        json_response = {}
    else:
        try:
            json_response: dict = resp.json()
        except json.decoder.JSONDecodeError as e:
            # Not valid JSON
            raise ErrorResponseException(resp, None, e)

    logging.debug(f"JSON response: {json_response}")

    if resp.status_code in code_to_dto_class:
        dto_class = code_to_dto_class[resp.status_code]

        # Due to the usage of data classes:
        # 1. Filter extra fields: avoid X.__init__() got an unexpected keyword argument 'X'
        # 2. Set missing fields to None: avoid "X.__init__() missing x required positional arguments"
        filtered_resp = {f.name: json_response.get(f.name, None) for f in fields(dto_class) if
                         not (f.name in {"resp_code", "response"})}

        if filtered_resp.keys() != json_response.keys():
            logging.warning(
                f"Response from {resp.url} differs from expected response. Difference in attributes: {filtered_resp.keys() ^ json_response.keys()}")

        return dto_class(resp_code=resp.status_code, response=resp, **filtered_resp)

    else:
        try:
            error_rsp = ErrorResp(**json_response)
            nested_exception = None
        except Exception as e:
            error_rsp = None
            nested_exception = e

        raise ErrorResponseException(resp, error_rsp, nested_exception)


def normalise_url(url: str) -> str:
    norm_url = url
    if not norm_url.startswith('http'):
        norm_url = 'https://' + norm_url
    return norm_url.rstrip('/')


def decode_token(token: str):
    # https://stackoverflow.com/questions/38683439/how-to-decode-base64-in-python3
    b64_string = token.split(".")[1]
    b64_string += "=" * ((4 - len(b64_string) % 4) % 4)
    return json.loads(base64.b64decode(b64_string))
