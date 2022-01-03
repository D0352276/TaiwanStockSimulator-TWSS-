from date_info import Date2YMD,ShiftDays

class StrategyBase:
    def __init__(self):
        self._past_price={}
        self._past_metrics={}
    def __call__(self,date,asset,price,metrics):
        self._Record(date,price,metrics)
        return self._Check(date,asset,price,metrics,self._past_price,self._past_metrics)
    def _Record(self,date,price,metrics):
        self._past_price[date]=price
        self._past_metrics[date]=metrics
        return
    def _Check(self,date,asset,price,metrics,past_price,past_metrics):
        year,month,day=Date2YMD(date)
        prncpl_money=asset["PrincipalMoney"]
        cur_money=asset["CurrentMoney"]
        cur_shares=asset["CurrentShares"]
        last_price=asset["LastBuyingPrice"]
        avg_price=asset["AvgPrice"]
        kd=metrics["KD"]
        last_day_price=past_price[ShiftDays(date,-1)]
        last_day_kd=past_metrics[ShiftDays(date,-1)]["KD"]
        buy_shares=1
        return buy_shares