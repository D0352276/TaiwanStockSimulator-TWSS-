from .strategy_base import StrategyBase
from date_info import Date2YMD

class KDSelling(StrategyBase):
    def __init__(self,buying_money):
        super(KDSelling,self).__init__()
        self._buying_money=buying_money
        self._over_buying_signal=False
    def _Check(self,date,asset,price,metrics,past_price,past_metrics):
        _year,_month,_day=Date2YMD(date)
        k,d=metrics["KD"]
        if(d<=80):self._over_buying_signal=False
        #selling check
        if(d>80 and self._over_buying_signal==False):
            self._over_buying_signal=True
        if(self._over_buying_signal==True and k<d):
            self._over_buying_signal=False
            return -asset["CurrentShares"]
        return 0