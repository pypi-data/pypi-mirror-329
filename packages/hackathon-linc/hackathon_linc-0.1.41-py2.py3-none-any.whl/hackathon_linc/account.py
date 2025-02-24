import requests
from . import ipaddr as ip_address
from typing import List, Dict, Union


def get_all_orders() -> List[Dict[str, Union[str, int, float]]]:
    """
    Returns a list of all completed and pending orders
    """
    return get_completed_orders() + get_pending_orders()


def get_completed_orders() -> List[Dict[str, Union[str, int, float]]]:
    """
    Returns a list of completed orders
    """
    url = ip_address.url + '/account/get_completed_orders'
    body = {"api_key": ip_address.token}
    response = requests.get(url, json=body)
    return response.json()


def get_pending_orders() -> List[Dict[str, Union[str, int, float]]]:
    """
    Returns a list of pending orders
    """
    url = ip_address.url + '/account/open_orders'
    body = {"api_key": ip_address.token}
    response = requests.get(url, json=body)
    return response.json()


def get_stoploss_orders() -> List[Dict[str, Union[str, int, float]]]:
    """
    Returns a list of stoploss orders
    """
    url = ip_address.url + '/account/get_stoploss_orders'
    body = {"api_key": ip_address.token}
    response = requests.get(url, json=body)
    return response.json()


def get_balance() -> float:
    """
    Returns a dictionary with the current balance
    """
    url = ip_address.url + f'/account/saldo'
    body = {"api_key": ip_address.token}
    response = requests.get(url, json=body)
    if response.status_code == 200:
        return response.json()['saldo']
    else:
        raise Exception(response.json())


def get_portfolio() -> Dict[str, int]:
    """
    Returns a dictionary with the amount of securities owned for each security
    """
    url = ip_address.url + '/account/portfolio'
    body = {"api_key": ip_address.token}
    response = requests.get(url, json=body)
    return response.json()
