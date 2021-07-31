import datetime

dt = datetime.datetime(2020, 1, 1)

for i in range(0,366):
    if dt.strftime("%A") not in ('Saturday', 'Sunday'):
        print(dt.strftime("%A"))
    dt = dt + datetime.timedelta(days=1)