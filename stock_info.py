import numpy as np
from json_io import JSON2Dict,Dict2JSON
from date_info import DateInfo,ShiftDays

def InitKD(closing_price_list,lowest_price_list,highest_price_list,ndate=9):
    class nDatePrice:
        def __init__(self,init_lowest,init_highest,ndate=9):
            self._ndate=ndate
            self._ndate_lowest_prices=[init_lowest for i in range(self._ndate)]
            self._ndate_highest_prices=[init_highest for i in range(self._ndate)]
        def Put(self,lowest_price,highest_price):
            self._ndate_lowest_prices.append(lowest_price)
            self._ndate_highest_prices.append(highest_price)
            del self._ndate_lowest_prices[0]
            del self._ndate_highest_prices[0]
        def HighestPrice(self):
            return max(self._ndate_highest_prices)
        def LowestPrice(self):
            return min(self._ndate_lowest_prices)
    kd_list=[]
    ndate_price_record=nDatePrice(init_lowest=lowest_price_list[0],init_highest=highest_price_list[0],ndate=ndate)
    last_k=0
    last_d=0
    for i,cur_closing_price in enumerate(closing_price_list):
        lowest_price=lowest_price_list[i]
        highest_price=highest_price_list[i]
        ndate_price_record.Put(lowest_price,highest_price)
        ndate_highest_price=ndate_price_record.HighestPrice()
        ndate_lowest_price=ndate_price_record.LowestPrice()
        rsv=(cur_closing_price-ndate_lowest_price)/(ndate_highest_price-ndate_lowest_price)*100
        cur_k=last_k*(2/3)+rsv*(1/3)
        cur_d=last_d*(2/3)+cur_k*(1/3)
        last_k=cur_k
        last_d=cur_d
        kd_list.append([cur_k,cur_d])
    return kd_list

class StockInfo:
    def __init__(self,stk_js_path):
        self._stk_js_path=stk_js_path
        self._stk_code=self._ParsingCode(stk_js_path)
        self._stk_dict=JSON2Dict(stk_js_path)
        self._InitCheck()
        self._dates2idx_dict=self._InitDate2IdxDict(self._stk_dict["Date"])
        self._begin_date=self._stk_dict["Date"][0]
        self._end_date=self._stk_dict["Date"][-1]
    def _ParsingCode(self,stk_js_path):
        code=stk_js_path.split(".")[0]
        code=code.split("/")
        try:code=code[1]
        except:code=code[0]
        return code
    def _InitCheck(self):
        if("KD" not in self._stk_dict):
            self._stk_dict["KD"]=InitKD(self._stk_dict["ClosingPrice"],
                                        self._stk_dict["LowestPrice"],
                                        self._stk_dict["HighestPrice"])
        if("MACD" not in self._stk_dict):
            pass
        Dict2JSON(self._stk_dict,self._stk_js_path)
    def _InitDate2IdxDict(self,dates):
        date2idx_dict={}
        for i,date in enumerate(dates):
            date2idx_dict[date]=i
        return date2idx_dict
    def _Date2Idx(self,date,interpolation=False):
        try:return self._dates2idx_dict[date]
        except:
            if(interpolation==False):
                raise Exception("StockInfo _Date2Idx Error: The date not in data.")
            elif(interpolation==True):
                if(DateInfo(date)-DateInfo(self._stk_dict["Date"][0])<0):
                    return self._dates2idx_dict[self._stk_dict["Date"][0]]
                if(DateInfo(self._stk_dict["Date"][-1])-DateInfo(date)<0):
                    return self._dates2idx_dict[self._stk_dict["Date"][-1]]
                while(date not in self._dates2idx_dict):
                    date=ShiftDays(date,-1)
                return self._dates2idx_dict[date]
            return
    def StkCode(self):
        return self._stk_code
    def DateByIdx(self,idx):
        try:return self._stk_dict["Date"][idx]
        except:raise Exception("StockInfo DateByIdx Error: The idx out of bound.")
    def ClosingPriceByIdx(self,idx):
        try:return self._stk_dict["ClosingPrice"][idx]
        except:raise Exception("StockInfo ClosingPriceByIdx Error: The idx out of bound.")
    def LowestPriceByIdx(self,idx):
        try:return self._stk_dict["LowestPrice"][idx]
        except:raise Exception("StockInfo LowestPriceByIdx Error: The idx out of bound.")
    def HighestPriceByIdx(self,idx):
        try:return self._stk_dict["HighestPrice"][idx]
        except:raise Exception("StockInfo HighestPriceByIdx Error: The idx out of bound.")
    def KDByIdx(self,idx):
        try:return self._stk_dict["KD"][idx]
        except:raise Exception("StockInfo KDByIdx Error: The idx out of bound.")
    def ClosingPriceByDate(self,date,interpolation=False):
        idx=self._Date2Idx(date,interpolation)
        try:return self._stk_dict["ClosingPrice"][idx]
        except:raise Exception("StockInfo ClosingPriceByDate Error: The idx out of bound.")
    def LowestPriceByDate(self,date,interpolation=False):
        idx=self._Date2Idx(date,interpolation)
        try:return self._stk_dict["LowestPrice"][idx]
        except:raise Exception("StockInfo LowestPriceByDate Error: The idx out of bound.")
    def HighestPriceByDate(self,date,interpolation=False):
        idx=self._Date2Idx(date,interpolation)
        try:return self._stk_dict["HighestPrice"][idx]
        except:raise Exception("StockInfo HighestPriceByDate Error: The idx out of bound.")
    def KDByDate(self,date,interpolation=False):
        idx=self._Date2Idx(date,interpolation)
        try:return self._stk_dict["KD"][idx]
        except:raise Exception("StockInfo KDByDate Error: The idx out of bound.")
    def BeginDate(self):
        return self._begin_date
    def EndDate(self):
        return self._end_date