#!/usr/bin/env python

"""
Tests for `linchackathon` package.

BE SURE TO add api key to self.group_token from database in order to test the functions.

Tests are very simple to ensure that basic functionality is in place.
"""
# Add the parent directory of your project to your Python path
import lincstem_hackathon as lh
from lincstem_hackathon import ipaddr as u
import unittest


class TestLinchackathon(unittest.TestCase):
    def setUp(self):
        self.group_token = 'ccc6816e-654d-4ecd-ac20-c7aba17cb0e9'
        u.token = self.group_token
        self.expected_tickers = ['STOCK1', 'STOCK2', 'STOCK3', 'STOCK4',
                                 'STOCK5', 'STOCK6', 'STOCK7', 'STOCK8', 'STOCK9', 'STOCK10']
        self.expected_tickers_length = len(self.expected_tickers)

    def test_init_success(self):
        lh.init(self.group_token)

    def test_init_invalid_input(self):
        with self.assertRaises(ValueError):
            lh.init(12345)

    def test_getTickers(self):

        returned_tickers = lh.get_tickers()
        self.assertEqual(self.expected_tickers.sort(), returned_tickers.sort())

    def test_getSecurityPrices(self):

        returned_prices = lh.get_security_prices()
        returned_length = len(returned_prices)

        self.assertEqual(self.expected_tickers_length, returned_length)

    def test_getHistoricSymbols(self):

        returned_historic_prices = lh.get_security_history()
        df = pd.DataFrame(returned_historic_prices)
        print(df.head())
        self.assertGreater(len(returned_historic_prices), 0)

    def test_getHistoricSymbols_faultyTicker(self):
        with self.assertRaises(ValueError):
            lh.getStockHistory(123)

    def test_getHistoricSymbols_faultyDaysBack(self):
        with self.assertRaises(ValueError):
            lh.getStockHistory(daysback=-2)

    def test_getHistoricSymbols_nonExistantTicker(self):
        with self.assertRaises(NameError):
            lh.getStockHistory("nonexistantstonk")
