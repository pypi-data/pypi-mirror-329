# -*- coding: utf-8 -*-
"""
Created on Wed Jan 13 11:08:56 2021

@author: yasse
"""


# =============================================================================
#  Imports
# =============================================================================
from typing import List
import requests
from . import ipaddr as u

# =============================================================================
# Getting all the tickers
# =============================================================================


def get_all_tickers() -> List[str]:
    """
    This function returns a list with all the tickers.

    """

    ticker_url = u.url+'/symbols'
    response = requests.get(ticker_url)
    response_json = response.json()

    return response_json


def get_current_price(ticker: str = None) -> dict:
    """
    This function takes in one argument, which is the ticker symbol, as a string 
    and returns the current price of the security. If no ticker is provided, 
    the function returns the current prices of all securities.

    Args:
        ticker (str, optional): The ticker symbol of the security. If no ticker is provided, the function returns the current prices of all securities.

    Returns:
        dict: A dictionary containing the current price of the security or securities.
    """
    gstock_url = u.url + '/data/stocks'
    params = {'ticker': ticker} if ticker else {}
    response = requests.get(gstock_url, params=params)
    return response.json()


def get_historical_data(days_back: int, ticker: str = None) -> dict:
    """
    This function gets historical data for tickers. If no ticker is specified it returns
    for all tickers. Requires days_back as a parameter and maximum 1 year back.

        Args:
            ticker : the ticker symbol or stock symbol (ex: STOCK1, STOCK2)
            daysback : an integer specifying the number of days to scrape from
                       in the past

    """
    if days_back < 0 or days_back > 365:
        raise ValueError("""
        You have entered a negative value for days back, it must be psotive.
        """)

    params = {'days_back': days_back}
    if ticker:
        params['ticker'] = ticker
    body = {"api_key": u.token}
    response = requests.get(u.url + '/data', params=params, json=body)

    return response.json()
