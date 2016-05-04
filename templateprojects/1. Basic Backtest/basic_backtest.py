import sys
import os

from pythonbacktest.datafeed import CSVDataFeed
from pythonbacktest.backtestengine import BasicBackTestEngine
from pythonbacktest.strategy import import_strategy
from pythonbacktest.broker import BackTestBroker
from pythonbacktest.tradelog import MemoryTradeLog

sys.path.append(os.path.abspath("../.."))

TEST_DATA_PATH = os.path.abspath("../testdata/ACME")
INITIAL_BUDGET = 100000

csv_data_feed = CSVDataFeed()
csv_data_feed.load_data(TEST_DATA_PATH)

trade_log = MemoryTradeLog()

broker = BackTestBroker(INITIAL_BUDGET, trade_log)

strategy_module = import_strategy(
    "basicSMAstrategy",
    os.path.abspath("basicsmastrategy.py"))

strategy = strategy_module.BasicSMAStrategy()

back_test_engine = BasicBackTestEngine(csv_data_feed, strategy, broker)
back_test_engine.start()

# testing done - let's display the final budget
print "Free cash: %s" % broker.free_cash

for transaction in trade_log.all_transactions:
    print "[%s] - %s@%s, remaining cash: %s" % \
          (transaction.timestamp, transaction.transaction_type,
           transaction.transaction_price_per_share, transaction.cash_after)

