import pandas as pd


def createApplierDF(question_list):
    columns = ["지원일자", "이름", "성별", "생년월일", "전화번호", "학교"]
    for question in question_list:
        columns.append(question.content)
    columns.append("선발여부")
    
    df = pd.DataFrame(columns=columns)
    return df


def addApplierDF(applier_query, df):
    for applier in applier_query:
        newdata = {}
        newdata["지원일자"]=applier.apply_date.strftime('%Y-%m-%d %H:%M:%S')
        newdata["이름"]=applier.name
        newdata["성별"]=applier.gender
        newdata["생년월일"]=str(applier.birth)
        newdata["전화번호"]=str(applier.phone)
        newdata["학교"]=applier.univ

        for answer in applier.answer.all():
            newdata[answer.question.content]=answer.answer           
            
        newdata["선발여부"]=applier.is_picked
        df = df.append(newdata, ignore_index=True)
        
    return df
