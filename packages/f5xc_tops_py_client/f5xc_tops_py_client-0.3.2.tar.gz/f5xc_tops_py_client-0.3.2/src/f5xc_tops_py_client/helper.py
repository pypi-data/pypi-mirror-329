"""Package helpers"""
import sys
from datetime import datetime
from uplink import retry, ratelimit, response_handler, error_handler

possible_keys = ['items', 'last_login_map', 'login_events_map', 'users']

def common_decorators(cls):
    """Function to package all uplink decorators for reuse"""
    decorators = [
        #returns.json,
        ratelimit(calls=50, period=50),
        xc_error_handler,
        xc_response_handler,
        xc_extract_items,
        retry(
            when=retry.when.status(503) | retry.when.status(429),
            stop=retry.stop.after_attempt(5) | retry.stop.after_delay(20),
            backoff=retry.backoff.jittered(multiplier=2)
        )
    ]
    for decorator in decorators:
        cls = decorator(cls)
    return cls

def tops_handler(exc_type, exc_value, tb, debug: bool = False):
    """Custom exception handler to give concise errors"""
    if debug:
        sys.__excepthook__(exc_type, exc_value, tb)
    else:
        print(f"{exc_type.__name__}: {exc_value}")

sys.excepthook = tops_handler

class TopsXCException(Exception):
    """Class to where all exceptions should rise"""

@response_handler
def xc_extract_items(json_data: dict):
    """Function to extract possible keys from response"""
    for key in possible_keys:
        if key in json_data:
            return json_data[key]
    return json_data

@response_handler
def xc_response_handler(response):
    """Function to handle HTTP responses"""
    if 200 <= response.status_code < 300:
        try:
            return response.json()
        except Exception as e:
            raise TopsXCException(f"Response not JSON: {str(e)}") from e
    try:
        error_data = response.json()
        error_message = error_data.get("message", "Unknown error occurred")
    except Exception:
        error_message = response.text
    raise TopsXCException(f"API ResponseCode {response.status_code}: {error_message}")

@error_handler(requires_consumer=True)
def xc_error_handler(consumer):
    """Function to handle HTTP client errors"""
    if isinstance(consumer.exceptions.BaseClientException):
        raise TopsXCException("BaseClientException")
    if isinstance(consumer.exceptions.ConnectionError):
        raise TopsXCException("ConnectionError")
    if isinstance(consumer.exceptions.ConnectionTimeout):
        raise TopsXCException("ConnectionTimeout")
    if isinstance(consumer.exceptions.ServerTimeout):
        raise TopsXCException("ServerTimeout")
    if isinstance(consumer.exceptions.SSLError):
        raise TopsXCException("SSLError")
    if isinstance(consumer.exceptions.InvalidURL):
        raise TopsXCException("InvalidURL")

def xc_filter_items(d: dict, keys: list) -> dict:
    """Fuction to filter XC reponse with 'items' dict"""
    items = d.get('items', [])
    filtered_items = [{key: d[key] for key in keys if key in d} for d in items]
    return {'items': filtered_items}

def xc_format_date(date_obj: datetime):
    """
    Function to format dates to what the console expects
    """
    return date_obj.strftime("%Y-%m-%dT%H:%M:%SZ")
