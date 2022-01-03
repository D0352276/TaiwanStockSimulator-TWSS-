from .strategy_base import StrategyBase

class SellingByProfit(StrategyBase):
    def __init__(self,profit_threshold=0.1):
        super(SellingByProfit,self).__init__()
        self._profit_threshold=profit_threshold
    def _Check(self,date,asset,price,metrics,past_price,past_metrics):
        cur_shares=asset["CurrentShares"]
        avg_price=asset["AvgPrice"]
        if(price/(avg_price+1e-8)>1+self._profit_threshold):
            return -cur_shares
        return 0