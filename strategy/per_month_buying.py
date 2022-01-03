from .strategy_base import StrategyBase
from date_info import Date2YMD

class PerMonthBuying(StrategyBase):
    def __init__(self,flat_month=3):
        super(PerMonthBuying,self).__init__()
        self._flat_month=flat_month
        self._last_itr_month=None
    def _Check(self,date,asset,price,metrics,past_price,past_metrics):
        _year,_month,_day=Date2YMD(date)
        self._buying_money=(asset["CurrentMoney"]//self._flat_month)*0.95
        if(self._last_itr_month!=_month):
            self._last_itr_month=_month
            if(asset["CurrentMoney"]>0):
                buy_shares=int(self._buying_money//price)
                return buy_shares
        return 0