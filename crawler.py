import os
import requests
import json
import time
from date_info import ShiftMonth,TodayDate,Date2YMD,YMD2Date
from json_io import Dict2JSON,JSON2Dict

def Get(stk_code,date,timeout=5,repeats=3):
    request_url="http://www.twse.com.tw/exchangeReport/STOCK_DAY?response=json&date="+str(date)+"&stockNo="+str(stk_code)+"&"
    data_dict=None
    for i in range(repeats):
        try:
            data=requests.get(request_url,timeout=timeout)
            time.sleep(timeout)
            data=data.text
            data_dict=json.loads(data)
            break
        except:pass
    if(data_dict==None):raise Exception("Get Error: It can't catch any data.")
    return data_dict

def CheckBeginDate(stk_code):
    cur_date=20100101
    data_dict=Get(stk_code,cur_date)
    while(data_dict["stat"]!="OK"):
        cur_date=ShiftMonth(cur_date,1)
        data_dict=Get(stk_code,cur_date)
    return cur_date

def CheckEndDate(stk_code):
    cur_date=TodayDate()
    y,m,d=Date2YMD(cur_date)
    cur_date=YMD2Date(y,m,1)
    data_dict=Get(stk_code,cur_date)
    while(data_dict["stat"]!="OK"):
        cur_date=ShiftMonth(cur_date,-1)
        data_dict=Get(stk_code,cur_date)
    return cur_date

def PreprocessingDataList(data_list):
    data_dict={}
    data_dict["Date"]=[]
    data_dict["NumberOfSharesTraded"]=[]
    data_dict["TransactionAmount"]=[]
    data_dict["OpeningPrice"]=[]
    data_dict["HighestPrice"]=[]
    data_dict["LowestPrice"]=[]
    data_dict["ClosingPrice"]=[]
    data_dict["NumberOfTransactions"]=[]
    for elemt_data in data_list:
        date=elemt_data[0]
        num_shares_traded=elemt_data[1]
        transaction_amount=elemt_data[2]
        opening_price=elemt_data[3]
        highest_price=elemt_data[4]
        lowest_price=elemt_data[5]
        closing_price=elemt_data[6]
        num_transactions=elemt_data[8]

        date=date.split("/")
        date=int(str(int(date[0])+1911)+date[1]+date[2])
        num_shares_traded=int(num_shares_traded.replace(",",""))
        transaction_amount=int(transaction_amount.replace(",",""))
        opening_price=float(opening_price)
        highest_price=float(highest_price)
        lowest_price=float(lowest_price)
        closing_price=float(closing_price)
        num_transactions=int(num_transactions.replace(",",""))
        
        data_dict["Date"].append(date)
        data_dict["NumberOfSharesTraded"].append(num_shares_traded)
        data_dict["TransactionAmount"].append(transaction_amount)
        data_dict["OpeningPrice"].append(opening_price)
        data_dict["HighestPrice"].append(highest_price)
        data_dict["LowestPrice"].append(lowest_price)
        data_dict["ClosingPrice"].append(closing_price)
        data_dict["NumberOfTransactions"].append(num_transactions)
    return data_dict

def CheckBeginEndDate(stk_code):
    begin_date=CheckBeginDate(stk_code)
    end_date=CheckEndDate(stk_code)
    return begin_date,end_date

def DownloadStkData(begin_date,end_date,stk_code):
    data_list=[]
    cur_date=begin_date
    data_dict=Get(stk_code,cur_date)
    data=data_dict["data"]
    data_list=data_list+data
    print("Download "+str(stk_code)+"......"+str(cur_date))
    while(cur_date!=end_date):
        cur_date=ShiftMonth(cur_date,1)
        data_dict=Get(stk_code,cur_date)
        data=data_dict["data"]
        data_list=data_list+data
        print("Download "+str(stk_code)+"......"+str(cur_date))
    data_dict=PreprocessingDataList(data_list)
    return data_dict

def MergeStkDatas(orig_dict,new_dict):
    out_dict={}
    orig_date_list=orig_dict["Date"]
    new_date_list=new_dict["Date"]
    new_date_begin=new_date_list[0]
    try:
        del_idx=orig_date_list.index(new_date_begin)
    except:del_idx=None
    for key in new_dict.keys():
        if(del_idx!=None):del orig_dict[key][del_idx:]
        out_dict[key]=orig_dict[key]+new_dict[key]
    return out_dict

def UpdateStkData(stk_code,dataset_dir):
    all_stk_files=os.listdir(dataset_dir)
    if(stk_code+".json" in all_stk_files):
        js_path=dataset_dir+"/"+stk_code+".json"
        js_dict=JSON2Dict(js_path)
        
        t_year,t_month,t_day=Date2YMD(TodayDate())
        year,month,day=Date2YMD(js_dict["Date"][-1])
        if(t_year!=year or t_month!=month or t_day!=day):
            begin_date,end_date=CheckBeginEndDate(stk_code)
            _data_dict=DownloadStkData(YMD2Date(year,month,1),end_date,stk_code)
            data_dict=JSON2Dict(dataset_dir+"/"+stk_code+".json")
            data_dict=MergeStkDatas(data_dict,_data_dict)
            Dict2JSON(data_dict,dataset_dir+"/"+stk_code+".json")
    else:
        data_dict=None
        begin_date,end_date=CheckBeginEndDate(stk_code)
        data_dict=DownloadStkData(begin_date,end_date,stk_code)
        Dict2JSON(data_dict,dataset_dir+"/"+stk_code+".json")
    return

