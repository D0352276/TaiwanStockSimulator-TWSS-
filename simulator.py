from date_info import DateInfo
from json_io import Dict2JSON

class Simulator:
    def __init__(self,stk_info,init_date=19110101,init_money=0,interpolation=True):
        self._stk_info=stk_info
        self._cur_date_info=DateInfo(date=init_date)
        self._principal_money=init_money
        self._cur_money=init_money
        self._cur_shares=0
        self._interpolation=interpolation
        self._last_buying_price=0
        self._avg_price=0
        self._check_income=None
        self._strtgy_funntions=[]
        self._op_logs=[]
        self._regular_logs=[]
    def _BuyingFee(self,deal_money):
        fee_rate=0.001425
        return deal_money*fee_rate
    def _SellingFee(self,deal_money):
        fee_rate=0.004425
        return deal_money*fee_rate
    def PushPrincipalMoney(self,in_money):
        self._cur_money+=in_money
        self._principal_money+=in_money
        self._op_logs.append([self.CurDate(),"Push",in_money,self._cur_money,self._cur_shares])
        return self._cur_money
    def BuyShares(self,num_shares):
        buying_price=self._stk_info.ClosingPriceByDate(self.CurDate(),self._interpolation)
        pay_money=num_shares*buying_price
        pay_money=pay_money+self._BuyingFee(pay_money)
        pay_money=round(pay_money)
        if(self._cur_money<pay_money):
            raise Exception("Simulator BuyShares Error: Current money is not enough.")
        self._cur_money=self._cur_money-pay_money
        self._last_buying_price=buying_price
        self._avg_price=(self._avg_price*self._cur_shares+num_shares*buying_price)/(self._cur_shares+num_shares)
        self._cur_shares+=num_shares
        self._op_logs.append([self.CurDate(),"Buy",pay_money,self._cur_money,self._cur_shares])
        return self._cur_money
    def AdaptBuyShares(self,pay_money):
        buying_price=self._stk_info.ClosingPriceByDate(self.CurDate(),self._interpolation)
        num_shares=(pay_money//buying_price)-1
        return self.BuyShares(num_shares)
    def SellShares(self,num_shares):
        if(num_shares==-1):num_shares=self._cur_shares
        if(self._cur_shares<num_shares or num_shares==0):
            raise Exception("Simulator SellShares Error: Current shares is not enough.")
        selling_price=self._stk_info.ClosingPriceByDate(self.CurDate(),self._interpolation)
        selling_money=num_shares*selling_price
        selling_money=selling_money-self._SellingFee(selling_money)
        selling_money=int(selling_money)
        self._cur_shares-=num_shares
        self._cur_money+=selling_money
        self._op_logs.append([self.CurDate(),"Sell",selling_money,self._cur_money,self._cur_shares])
        return self._cur_money
    def CurAsset(self):
        asset_dict={}
        asset_dict["PrincipalMoney"]=self._principal_money
        asset_dict["CurrentMoney"]=self._cur_money
        asset_dict["CurrentShares"]=self._cur_shares
        asset_dict["LastBuyingPrice"]=self._last_buying_price
        asset_dict["AvgPrice"]=self._avg_price
        return asset_dict
    def SetRegularIncome(self,day,regular_money):
        def _CheckIncome():
            _year,_month,_day=self._cur_date_info.CurDateYMD()
            if(_day==day):
                self.PushPrincipalMoney(regular_money)
            return
        self._check_income=_CheckIncome
    def AddStrategy(self,strtgy_funntion):
        self._strtgy_funntions.append(strtgy_funntion)
        return
    def NextDay(self):
        self._cur_date_info.ShiftDays(days=1)
        try:self._check_income()
        except:pass
        try:
            date=self._cur_date_info.CurDate()
            closing_price=self._stk_info.ClosingPriceByDate(date,self._interpolation)
            self._regular_logs.append([self.CurDate(),closing_price,
                                       self._avg_price,self._cur_money,
                                       self._cur_shares,self._principal_money])
        except:return
        tech_metrics={}
        tech_metrics["KD"]=self._stk_info.KDByDate(date,self._interpolation)
        
        for strtgy_funntion in self._strtgy_funntions:
            args=(date,self.CurAsset(),closing_price,tech_metrics)
            buy_shares=strtgy_funntion(*args)
            if(buy_shares>0):self.BuyShares(buy_shares)
            elif(buy_shares<0):self.SellShares(int(buy_shares*(-1)))
        return
    def BeginDate(self):
        return self._stk_info.BeginDate()
    def EndDate(self):
        return self._stk_info.EndDate()
    def CurDate(self):
        return self._cur_date_info.CurDate()
    def CurProfit(self):
        return (self._cur_money/self._principal_money)-1
    def Logs(self):
        logs={}
        logs["Code"]=self._stk_info.StkCode()
        logs["RegularLogs"]=self._regular_logs
        logs["OPLogs"]=self._op_logs
        return logs