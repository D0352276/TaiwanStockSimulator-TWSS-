import datetime

class DateInfo:
    def __init__(self,date=19110101):
        if(date//10000000>2):
            raise Exception("DateInfo __init__ Error: The arg 'date' out of bound.")
        self._date=date
    def __sub__(self,date_info):
        cur_date=self._date
        target_date=date_info._date
        cur_date=datetime.date(*self._Date2YMD(cur_date))
        target_date=datetime.date(*self._Date2YMD(target_date))
        gap_days=(cur_date-target_date).days
        return gap_days
    def _Date2YMD(self,date):
        year=date//10000
        cur_val=date-year*10000
        month=cur_val//100
        day=cur_val-month*100
        return year,month,day
    def _YMD2Date(self,year,month,day):
        date=year*10000+month*100+day
        return date
    def ShiftDays(self,days=1):
        date=datetime.date(*self._Date2YMD(self._date))
        date+=datetime.timedelta(days=days)
        self._date=self._YMD2Date(date.year,date.month,date.day)
        return self
    def ShiftMonth(self,month=1):
        y,m,d=self._Date2YMD(self._date)
        m+=month
        if(m==13):
            y+=1
            m=1
        elif(m==0):
            y-=1
            m=12
        self._date=self._YMD2Date(y,m,d)
        return self
    def CurDate(self):
        return self._date
    def CurDateYMD(self):
        return self._Date2YMD(self._date)

def ShiftDays(date,days):
    date_info=DateInfo(date)
    date_info.ShiftDays(days)
    return date_info.CurDate()

def ShiftMonth(date,month):
    date_info=DateInfo(date)
    date_info.ShiftMonth(month)
    return date_info.CurDate()

def Date2YMD(date):
    date_info=DateInfo(date)
    return date_info.CurDateYMD()

def YMD2Date(year,month,day):
    date=year*10000+month*100+day
    return date

def TodayDate():
    today_date=datetime.date.today()
    today_date=today_date.__str__().split("-")
    date=today_date[0]+today_date[1]+today_date[2]
    return int(date)