from stock_info import StockInfo
from simulator import Simulator
from strategy import PerMonthBuying,SellingByProfit
from logs_io import Logs2Fig,SaveLogs,LoadLogs
from crawler import UpdateStkData

stock_code="0050"
data_path="dataset/"+stock_code+".json"
init_date=20180101
income_day=20
tot_date_len=1500
update=True

#update data
if(update==True):
    UpdateStkData(stock_code,"dataset")

#init stategy
buy_strategy=PerMonthBuying(flat_month=2)
sell_strategy=SellingByProfit(0.5)

# init stock data
stk_info=StockInfo(data_path)
# init simulator
simulator=Simulator(stk_info,init_date)
# set income date and money
simulator.SetRegularIncome(day=20,regular_money=5000)
simulator.AddStrategy(buy_strategy)
simulator.AddStrategy(sell_strategy)

for i in range(tot_date_len):
    simulator.NextDay()
simulator.SellShares(-1)
print("Profit:",simulator.CurProfit())

logs=simulator.Logs()
SaveLogs(logs,"demo/logs.json")
logs=LoadLogs("demo/logs.json")
Logs2Fig(logs,"demo/logs.png")
