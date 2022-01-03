from .strategy_base import StrategyBase
from date_info import Date2YMD

class KDBuying(StrategyBase):
    def __init__(self,atleast_money=5000):
        super(KDBuying,self).__init__()
        self._atleast_money=atleast_money
        self._over_selling_signal=False
    def _Check(self,date,asset,price,metrics,past_price,past_metrics):
        _year,_month,_day=Date2YMD(date)
        k,d=metrics["KD"]
        if(d>=20):self._over_selling_signal=False
        #buying check
        if(d<20 and self._over_selling_signal==False):
            self._over_selling_signal=True
        if(self._over_selling_signal==True and k>d and asset["CurrentMoney"]>self._atleast_money):
            buy_shares=int((asset["CurrentMoney"]*0.95)//price-1)
            self._over_selling_signal=False
            return buy_shares
        return 0

