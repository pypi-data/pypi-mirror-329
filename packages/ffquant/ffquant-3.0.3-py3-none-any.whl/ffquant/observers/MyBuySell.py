import backtrader as bt
import pytz
import ffquant.utils.global_backtest_data as global_backtest_data
from backtrader.lineiterator import LineIterator

__ALL__ = ['MyBuySell']

# 用于记录买卖点、指标的值的信息
class MyBuySell(bt.observers.BuySell):

    def __init__(self):
        super(MyBuySell, self).__init__()
        self.buysells = global_backtest_data.buysells
        self.indcs = global_backtest_data.indcs

    def start(self):
        super(MyBuySell, self).start()
        self.buysells.clear()

        strategy = self._owner
        for ind in strategy._lineiterators[LineIterator.IndType]:
            existing_cnt = 0
            for k, v in self.indcs.items():
                if k == ind.__class__.__name__ or k.startswith(f"{ind.__class__.__name__}-"):
                    existing_cnt += 1
            if existing_cnt > 0:
                self.indcs[f"{ind.__class__.__name__}-{existing_cnt + 1}"] = []
            else:
                self.indcs[ind.__class__.__name__] = []

    # 这个next方法会在策略的next方法之后执行
    def next(self):
        super(MyBuySell, self).next()

        for i in range(0, len(self.datas)):
            symbol = self.datas[i].p.symbol
            symbol_buysells = self.buysells.get(symbol, [])

            msg = {
                "datetime": self.datas[i].datetime.datetime(0).replace(tzinfo=pytz.utc).astimezone().strftime("%Y-%m-%d %H:%M:%S"),
                "price": self.datas[i].close[0],
                "buy": self.lines.buy[0],
                "sell": self.lines.sell[0]
            }
            symbol_buysells.append(msg)
            self.buysells[symbol] = symbol_buysells

        indc_cnt_dict = {}
        strategy = self._owner
        for indc in strategy._lineiterators[LineIterator.IndType]:
            key = indc.__class__.__name__
            if indc_cnt_dict.get(indc.__class__.__name__, 0) > 0:
                key = f"{indc.__class__.__name__}-{indc_cnt_dict.get(indc.__class__.__name__, 0) + 1}"
            indc_cnt_dict[indc.__class__.__name__] = indc_cnt_dict.get(indc.__class__.__name__, 0) + 1

            history_values = self.indcs[key]
            history_values.append(indc[0])