from django.db.models import query
from numpy import string_
import pandas as pd

def makeApplierDF(question_list):
    columns = ["지원일자", "이름", "성별", "생년월일", "전화번호"]
    for question in question_list:
        columns.append(question.content)
    columns.append("선발여부")
    
    df = pd.DataFrame(columns=columns)
    return df
