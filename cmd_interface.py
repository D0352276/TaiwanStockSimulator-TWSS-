import argparse
from cfg_parser import ParsingCfg
from import_strategy import ImportStrategy
from stock_info import StockInfo
from simulator import Simulator
from logs_io import SaveLogs,Logs2Fig
from crawler import UpdateStkData

if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument("cfg_path",help="config file path",type=str)
    args=parser.parse_args()
    cfg_dict=ParsingCfg(args.cfg_path)

    stock_code=cfg_dict["stock_code"]
    init_date=int(cfg_dict["init_date"])
    date_len=int(cfg_dict["date_len"])
    init_money=cfg_dict["init_money"]
    income_day=cfg_dict["income_day"]
    regular_money=cfg_dict["regular_money"]
    interpolation=cfg_dict["interpolation"]
    update=cfg_dict["update"]
    strategy_list=cfg_dict["strategy_list"]
    logs_path=cfg_dict["logs_path"]
    fig_path=cfg_dict["fig_path"]
    

    if(update==True):
        UpdateStkData(stock_code)

    # init stock data
    stk_info=StockInfo("dataset/"+stock_code+".json")
    # init simulator
    simulator=Simulator(stk_info,init_date,init_money=init_money,interpolation=interpolation)
    # set income date and money
    simulator.SetRegularIncome(day=income_day,regular_money=regular_money)
    for strategy_name in strategy_list:
        simulator.AddStrategy(ImportStrategy("strategy",strategy_name)())

    for i in range(date_len):
        simulator.NextDay()
    simulator.SellShares(-1)
    print("Profit:",simulator.CurProfit())

    logs=simulator.Logs()
    SaveLogs(logs,logs_path)
    Logs2Fig(logs,fig_path)
