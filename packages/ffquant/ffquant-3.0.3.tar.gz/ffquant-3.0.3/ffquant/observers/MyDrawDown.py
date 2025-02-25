import backtrader as bt
import pytz
import ffquant.utils.global_backtest_data as global_backtest_data

__ALL__ = ['MyDrawDown']

class MyDrawDown(bt.observers.DrawDown):
    def __init__(self):
        super(MyDrawDown, self).__init__()
        self.drawdowns = global_backtest_data.drawdowns

    def start(self):
        super(MyDrawDown, self).start()
        self.drawdowns.clear()

    # 这个next方法会在策略的next方法之后执行
    def next(self):
        super(MyDrawDown, self).next()

        msg = {
            "datetime": self.data.datetime.datetime(0).replace(tzinfo=pytz.utc).astimezone().strftime("%Y-%m-%d %H:%M:%S"),
            "drawdown": self.lines.drawdown[0]
        }
        self.drawdowns.append(msg)
