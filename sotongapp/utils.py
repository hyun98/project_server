from datetime import datetime
from datetime import date
import pandas as pd

from django.db.models import Q

from sotongapp.models import Organ, Information

def get_maxvnum_avgnum(total, organ):
    startdate = date(2021, 8, 16)
    enddate = datetime.date(datetime.today())
    daterange = pd.date_range(startdate, enddate, freq='D')
    
    day_total = 0
    max_visitor = 0
    
    for day in daterange:
        day_query_count = Information.objects.filter(Q(organ=organ) & Q(day=day)).count()
        if day_query_count > 0:
            day_total += 1
            max_visitor = max(max_visitor, day_query_count)
    
    avg_user_num = round(total / day_total, 2)
    
    return avg_user_num, max_visitor