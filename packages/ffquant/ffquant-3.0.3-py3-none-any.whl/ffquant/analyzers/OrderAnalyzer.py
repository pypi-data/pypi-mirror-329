import backtrader as bt
import pytz
import ffquant.utils.global_backtest_data as global_backtest_data

__ALL__ = ['OrderAnalyzer']

class OrderAnalyzer(bt.Analyzer):
    def __init__(self):
        self.orders = global_backtest_data.orders
    
    def start(self):
        super(OrderAnalyzer, self).start()
        self.orders.clear()

    # 当订单的状态变化时 该方法会被调用
    # 该方法的调用时机是策略的next方法被调用之前
    def notify_order(self, order):
        if order.status == order.Completed or (order.exectype == order.Limit and (order.status == order.Submitted or order.status == order.Cancelled)):
            symbol = order.data.p.symbol
            symbol_orders = self.orders.get(symbol, [])

            dt = self.data.datetime.datetime(0).replace(tzinfo=pytz.utc).astimezone().strftime("%Y-%m-%d %H:%M:%S")
            # 这里的position_after有个问题 当有多个订单时 position_after代表的其实是所有订单成交后的仓位信息 而不是单个订单成交后的仓位信息
            oinfo = {
                'datetime': dt,
                'data': order,
            }
            symbol_orders.append(oinfo)
            self.orders[symbol] = symbol_orders

    def get_analysis(self):
        return self.orders