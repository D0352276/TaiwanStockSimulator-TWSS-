# TaiwanStockSimulator-TWSS-

TWSS是一個基於台股每日收盤價回測程式交易策略的模擬器，TWSS提供了一套簡潔的API使撰寫並測試自定義的交易策略變得十分容易。

## Requirements

- [Python 3](https://www.python.org/)
- [Matplotlib](https://matplotlib.org/)
- [Numpy](http://www.numpy.org/)


## Quick Start
```bash
#Predict
python3 main.py -p cfg/predict_coco.cfg

#Train
python3 main.py -t cfg/train_coco.cfg

#Eval
python3 main.py -ce cfg/eval_coco.cfg
```


## Customize Your Strategy

我們在strategy.py中提供了基礎的虛擬類別StrategyBase，只需要繼承該類別並重新撰寫_Check(...)函數就可以自定義任意策略。

這裡展示了定期定額的買入策略：

```bash
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
需要注意的是_Check(...)的接口必須維持一致不得任意改變，傳入值分別代表的意義如下
- **asset(dict):** 傳入當前的剩餘金錢，持有股數等資訊
- **price(float):** 當日的收盤價
- **metrics(dict):** 多種技術指標，目前只提供了KD
- **past_price(dict):** 歷史上的每日收盤價，key值為日期
- **past_metrics(dict):** 歷史上的每日技術指標，key值為日期

## More Info



## TODOs

- Improve the calculator script of FLOPs.
- Using Focal Loss will cause overfitting, we need to explore the reasons.
