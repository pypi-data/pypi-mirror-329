"""
Tests for `linchackathon` package.

BE SURE TO add api key to self.group_token from database in order to test the functions.

Tests are very simple to ensure that basic functionality is in place.
RUN test 1 by 1 to check that everything works, bit goofy but hey.
"""
# Add the parent directory of your project to your Python path
import lincstem_hackathon as lh
from lincstem_hackathon import ipaddr as u
import unittest


class TestLinchackathon(unittest.TestCase):
    def __init__(self, methodName):
        super().__init__(methodName)
        self.expected_orders_completed = 0
        self.expected_orders_pending = 0

    def setUp(self):
        self.group_token = 'bbdde9e8-5bce-482b-b9c3-16b7f86f55db'
        self.starting_saldo = 10000  # HARDCODED
        u.token = self.group_token
        self.expected_tickers = ['STOCK1', 'STOCK2', 'STOCK3', 'STOCK4',
                                 'STOCK5', 'STOCK6', 'STOCK7', 'STOCK8', 'STOCK9', 'STOCK10']
        self.expected_tickers_length = len(self.expected_tickers)

    def test_init_success(self):
        lh.init(self.group_token)

    def test_completedOrders_empty(self):
        returned_orders = lh.get_completed_orders()
        self.assertEqual(len(returned_orders), 0)

    def test_pendingOrders_empty(self):
        returned_orders = lh.get_pending_orders()
        self.assertEqual(len(returned_orders), 0)

    def test_add_pendingOrder(self):
        symbol = "STOCK1"
        amount = 1
        price = 1  # Price we never will buy at
        result = lh.place_buy_order(
            symbol, amount, price, days_to_cancel=40000)
        if result:
            self.expected_orders_pending += 1

        pending_orders = lh.get_pending_orders()
        self.assertEqual(len(pending_orders), self.expected_orders_pending)

    def test_placeBuyOrder(self):
        symbol = "STOCK2"
        amount = 1
        price = 5000  # Price we will buy at

        result = lh.place_buy_order(symbol, amount, price)
        result_str = result[0:6]
        self.assertEqual(result_str, '{"amou')

    def test_placeSellOrder(self):
        symbol = "STOCK2"
        amount = 1
        price = 0  # Price we sell at

        result = lh.place_sell_order(symbol, amount, price)
        result_str = result[0:6]
        self.assertEqual(result_str, '{"amou')

    def test_buySecurity(self):
        symbol = "STOCK8"
        amount = 1
        result = lh.buy_security(symbol, amount)
        result_str = result[0:6]
        self.assertEqual(result_str, '{"amou')

    def test_sellSecurity(self):
        symbol = "STOCK8"
        amount = 1
        result = lh.sell_security(symbol, amount)
        result_str = result[0:6]
        self.assertEqual(result_str, '{"amou')

    def test_placeSellOrder_notOwned(self):
        # SELLING STOCK WE DONT OWN TEST
        symbol = "STOCK5"
        amount = 1
        price = 2  # Price we will sell at

        result = lh.place_sell_order(symbol, amount, price)
        result_str = result[0:6]
        self.assertEqual(result_str, '(psyco')

    def test_getSaldo(self):
        result = lh.get_saldo()
        saldo = result['saldo']

        self.assertGreaterEqual(saldo, 0, msg="saldo not recieved")

    def test_getPortfolio(self):
        result = lh.get_portfolio()
        portfolio_size = sum(result.values())
        self.assertEqual(portfolio_size, 0)

    def test_cancel_order(self):
        symbol = "STOCK1"
        amount = 1
        price = 2

        place_order = lh.place_buy_order(symbol, amount, price)
        cancel_order = lh.cancel_order(symbol)

        place_order_str = place_order[0:6]
        cancel_order_str = cancel_order[0:6]

        self.assertEqual(cancel_order_str, '{\"mess')
        self.assertEqual(place_order_str, '{\"amou')

    def test_stopLoss(self):
        symbol = "STOCK2"
        amount = 1
        price = 2

        place_order = lh.place_buy_order(symbol, amount, 2000)
        stoploss_order = lh.place_stoploss_order(symbol, amount, price)

        place_order_str = place_order[0:6]
        cancel_order_str = stoploss_order[0:6]

        self.assertEqual(cancel_order_str, '{\"amou')
        self.assertEqual(place_order_str, '{\"amou')
