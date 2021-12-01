import pandas as pd

from survey.models import Answer


def createApplierDF(question_list):
    columns = ["지원일자", "이름", "성별", "생년월일", "전화번호"]
    for question in question_list:
        columns.append(question.content)
    columns.append("선발여부")
    
    df = pd.DataFrame(columns=columns)
    return df


def addApplierDF(applier_query, df, survey):
    for applier in applier_query:
        newdata = {}
        newdata["지원일자"]=applier.apply_date.strftime('%Y-%m-%d %H:%M:%S')
        newdata["이름"]=applier.name
        newdata["성별"]=applier.gender
        newdata["생년월일"]=applier.birth
        newdata["전화번호"]=applier.phone
        
        answer_list = Answer.objects.select_related(
                'question'
            ).\
            filter(
                survey=survey,
                applier=applier
            )
        for answer in answer_list:
            newdata[answer.question.content]=answer.answer           
            
        newdata["선발여부"]=applier.is_picked
        df = df.append(newdata, ignore_index=True)
        
    return df
