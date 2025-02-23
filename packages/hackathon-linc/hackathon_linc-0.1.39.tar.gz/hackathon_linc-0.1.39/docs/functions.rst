functions
=======

The `account` module contains functions for accessing account-related data.

Functions
---------

``get_all_orders()``
    Returns a list of all completed and pending orders.

``get_completed_orders()``
    Returns a list of completed orders.

``get_pending_orders()``
    Returns a list of pending orders.

``get_stoploss_orders()``
    Returns a list of stoploss orders.

``get_balance()``
    Returns the current balance as a float.

``get_portfolio()``
    Returns a dictionary with the amount of securities owned for each security.

auth
====

The `auth` module contains functions for authenticating the user's token.

Functions
---------

``init(group_token: str)``
    Initializes the connection and authenticates the token.

Raises:
    ValueError: If the token is not a string.
    NameError: If the token is not valid.

Returns:
    None: Prints a welcome message.


historic.data
=============

The `historic.data` module contains functions for accessing historical data.

Functions
---------

``get_all_tickers()``
    Returns a list with all the tickers.

``get_current_price(ticker: str = None)``
    Returns the current price of the security or securities.

Args:
    ticker (str, optional): The ticker symbol of the security. If no ticker is provided, the function returns the current prices of all securities.

``get_historical_data(days_back: int, ticker: str = None)``
    Gets historical data for tickers.

Args:
    ticker : the ticker symbol or stock symbol (ex: STOCK1, STOCK2)
    daysback : an integer specifying the number of days to scrape from in the past.


transaction
===========

The `transaction` module contains functions for buying, selling, and placing stoploss orders.

Functions
---------

``buy(ticker: str, amount: int, price: Union[int, None] = None, days_to_cancel: int = 30)``
    Places a buy order for a given security.

``sell(ticker: str, amount: int, price: Union[int, None] = None, days_to_cancel: int = 30)``
    Places a sell order for a given security.

``stoploss(ticker: str, amount: int, price: float, days_to_cancel: int = 30)``
    Places a stoploss order for a given security.

``cancel(order_id: Union[int, None] = None, ticker: Union[str, None] = None)``
    Cancels a specific order or all orders for a given security.
