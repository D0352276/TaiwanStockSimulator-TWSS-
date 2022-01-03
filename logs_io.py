import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
from date_info import Date2YMD
from json_io import Dict2JSON,JSON2Dict

def PreprocessLogs(logs):
    regular_logs=logs["RegularLogs"]
    op_logs=logs["OPLogs"]

    _date_list=list(map(lambda x:x[0],regular_logs))

    date_list=[]
    for date in _date_list:
        y,m,d=Date2YMD(date)
        date_str=str(y)+"-"+str(m)+"-"+str(d)
        date_list.append(date_str)
    prices=list(map(lambda x:x[1],regular_logs))
    prices_x=date_list
    prices_y=prices

    avg_prices=list(map(lambda x:x[2],regular_logs))
    avg_prices_x=[]
    avg_prices_y=[]
    for i,avg_p in enumerate(avg_prices):
        if(avg_p==0):continue
        avg_prices_x.append(date_list[i])
        avg_prices_y.append(avg_p)

    ops_count=0
    buy_x=[]
    buy_y=[]
    sell_x=[]
    sell_y=[]
    for i,date in enumerate(_date_list):
        while(1):
            try:
                op_date=op_logs[ops_count][0]
                op_type=op_logs[ops_count][1]
            except:break
            if(op_date==date and op_type=="Buy"):
                buy_x.append(i)
                buy_y.append(prices[i])
                ops_count+=1
            elif(op_date==date and op_type=="Sell"):
                sell_x.append(i)
                sell_y.append(prices[i])
                ops_count+=1
            elif(op_date<=date):
                ops_count+=1
            else:
                break

    cur_mny_y=list(map(lambda x:x[3],regular_logs))
    min_cur_m=min(cur_mny_y)
    max_cur_m=regular_logs[-1][-1]
    min_price=min(prices_y)
    max_price=max(prices_y)
    cur_mny_x=prices_x
    scale_factor=(max_price-min_price)/(max_cur_m-min_cur_m)
    cur_mny_y=list(map(lambda x:scale_factor*(x-max_cur_m)+max_price,cur_mny_y))
    return (prices_x,prices_y),(avg_prices_x,avg_prices_y),(cur_mny_x,cur_mny_y),(buy_x,buy_y),(sell_x,sell_y)
    
def Logs2Fig(logs,save_path,interval=20):
    prices,avg_prices,cur_mny,buy_point,sell_point=PreprocessLogs(logs)
    fig,ax=plt.subplots(figsize=(15,8))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=max(len(prices[0])//interval,interval)))
    plt.plot(*prices,"-",color="#808080",alpha=0.5,linewidth=2,label="Current Price")
    plt.plot(*avg_prices,"--",color="#ff2d51",alpha=0.75,linewidth=2,label="Buying Avg Price")
    plt.plot(*cur_mny,"-",color="#ff6103",alpha=0.65,linewidth=2,label="Relative Res Money")
    plt.plot(*buy_point,"x",color="#ff2d51",markersize=10,label="Buying Point")
    plt.plot(*sell_point,"x",color="#057748",markersize=10,label="Selling Point")
    plt.gcf().autofmt_xdate()
    leg=ax.legend(loc='upper left',shadow=False)
    plt.title(logs["Code"])
    plt.ylabel("Price")
    plt.savefig(save_path)
    return

def SaveLogs(logs,out_path):
    Dict2JSON(logs,out_path)
    return
    
def LoadLogs(logs_path):
    return JSON2Dict(logs_path)