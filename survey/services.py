from django.db.models import query
import pandas as pd

def makeApplierDF(question_list):
    applierDf = pd.DataFrame({
        "지원일자": [],
        "이름": [],
        "성별": [],
        "생년월일": [],
        "전화번호": [],
    })
    for question in question_list:
        print(question.content)
        applierDf[question.content] = []
    applierDf["선발여부"] = []
    
    return applierDf
