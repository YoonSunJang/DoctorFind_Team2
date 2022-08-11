from datetime import datetime
from dateutil.relativedelta import relativedelta

my_date = datetime(2019,10,10)
new_date1 = my_date + relativedelta(months=4)
new_date2 = my_date + relativedelta(days=-10)
print(new_date1)
print(new_date2)