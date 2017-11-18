from abc import ABC, abstractmethod

from ai.backoffice.tradehistory import TradeHistory
from ai.strategyperformance import PerformanceReport


class AbstractPerfCalculator(ABC):

    @abstractmethod
    def calculate_strategy_performance(self, trade_history: TradeHistory) -> PerformanceReport:
        raise NotImplementedError()
