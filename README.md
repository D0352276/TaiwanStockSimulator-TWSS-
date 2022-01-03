# TaiwanStockSimulator-TWSS-

![](https://img.shields.io/badge/Python-3-blue)
[![license](https://img.shields.io/github/license/mashape/apistatus.svg)](LICENSE)

TWSS是一個基於台股每日收盤價回測程式交易策略的模擬器，TWSS提供了簡潔的API以及CLI使撰寫自定義交易策略並測試變得十分容易。
<div align=center>
<img src=https://github.com/D0352276/TaiwanStockSimulator-TWSS-/blob/main/demo/logs.png width=100% />
</div>


## Requirements

- [Python 3](https://www.python.org/)
- [Matplotlib](https://matplotlib.org/)
- [Numpy](http://www.numpy.org/)


## Quick Start

我們提供了兩個界面(CLI/API)供不同類型的使用者選擇。

CLI的使用方式是撰寫cfg檔，並經由cmd_interface.py解析即可。

我們已經提供了demo用的cfg，可以藉由觀察cfg的撰寫以及執行以下指令進一步學習如何使用CLI：

```bash
python3 cmd_interface.py cfg/demo.cfg
```
執行完的輸出圖表如頁首所示。
- **灰色線:** 每日的收盤價
- **紅色X:** 買入的時間點
- **綠色X:** 賣出的時間點
- **紅色虛線:** 持有股票的均價
- **橘色線(0~1):** 可用金錢的相對值，越靠近1代表越多可用金錢未被投入市場

API界面的範例則寫在api_example.py裡頭，裡面同楊提供了簡潔的demo程式碼，請閱讀並執行以了解使用細節：

```bash
python3 api_example.py
```

## Customize Your Strategy

我們在strategy.py中提供了基礎的虛擬類別StrategyBase，只需要繼承該類別並重新撰寫_Check(...)函數就可以自定義任意策略。

這裡展示了定期定額的買入策略：

```Python
class PerMonthBuying(StrategyBase):
    def __init__(self,flat_month=3):
        super(PerMonthBuying,self).__init__()
        self._flat_month=flat_month
        self._last_itr_month=None
    def _Check(self,date,asset,price,metrics,past_price,past_metrics):
        _year,_month,_day=Date2YMD(date)
        self._buying_money=(asset["CurrentMoney"]//self._flat_month)*0.95
        if(self._last_itr_month!=_month):
            self._last_itr_month=_month
            if(asset["CurrentMoney"]>0):
                buy_shares=int(self._buying_money//price)
                return buy_shares
        return 0
```

需要注意的是_Check(...)的接口必須維持一致不得任意改變，傳入值分別代表的意義如下：

- **asset(dict):** 傳入當前的剩餘金錢，持有股數等資訊
- **price(float):** 當日的收盤價
- **metrics(dict):** 多種技術指標，目前只提供了KD
- **past_price(dict):** 歷史上的每日收盤價，key值為日期
- **past_metrics(dict):** 歷史上的每日技術指標，key值為日期

函數_Check(...)回傳值為正/負整數，分別代表買入或賣出整數股。

自定義的strategy必須為一個單獨的.py檔案並放置在strategy資料夾中，如此一來就可以在API或CLI界面直接呼叫使用了。
```Python
#API
from strategy import YourStrategy
```

```bash
#cfg of CLI
strategy_list=["YourStrategy"]
```

## More Info
