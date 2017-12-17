import sys
import os

sys.path.append(os.path.abspath("../.."))

from pythonbacktest.datafeed import CSVDataFeed
from pythonbacktest.backtestengine import BasicBackTestEngine
from pythonbacktest.strategy import import_strategy
from pythonbacktest.broker import BackTestBroker
from pythonbacktest.tradelog import MemoryTradeLog
from pythonbacktest.indicatorshistory import IndicatorHistory
from pythonbacktest.animation import IndicatorsHistoryAnimation

from datetime import date


TEST_DATA_PATH = os.path.abspath("../testdata/ACME")
INITIAL_BUDGET = 100000
DATE_TO_ANALYSIS = date(2016,1,2)

csv_data_feed = CSVDataFeed()
csv_data_feed.load_data(TEST_DATA_PATH)

trade_log = MemoryTradeLog()

broker = BackTestBroker(INITIAL_BUDGET, trade_log=trade_log, commision=1.0)

strategy_module = import_strategy(
    "basicSMAstrategy",
    os.path.abspath("basicsmastrategy.py"))

strategy = strategy_module.BasicSMAStrategy()

indicator_history = IndicatorHistory()

back_test_engine = BasicBackTestEngine(csv_data_feed, strategy, broker, indicator_history)
back_test_engine.start()

# testing done - let's display the final budget
print "Free cash: %s" % broker.free_cash

for transaction in trade_log.all_transactions:
    print "[%s] - %s@%s, remaining cash: %s" % \
          (transaction.timestamp, transaction.transaction_type,
           transaction.transaction_price_per_share, transaction.cash_after)

indicators_to_display = [('close', 'gray'),
                         ('SMA200', 'blue'),
                         ('SMA50', 'orange')]

volume_indicators = [('volume', 'red')]

# let's introduce an animation
indicators_animation = IndicatorsHistoryAnimation(indicator_history, DATE_TO_ANALYSIS,
                                                  canvassize=(10,10),
                                                  markers=['trade_buy', 'trade_sell'],
                                                  indicators=[indicators_to_display, volume_indicators])
indicators_animation.start_animation()