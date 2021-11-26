from rest_framework import serializers

from survey.models import *


class SubQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubQuestion
        fields = '__all__'
    
    
class QuestionSerializer(serializers.ModelSerializer):
    sub_question = SubQuestionSerializer(many=True)
    
    class Meta:
        model = Question
        fields = 'id', 'content', 'order', 'is_multichoice', \
            'can_duplicate', 'survey', 'sub_question'
            

class SurveyFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = SurveyFile
        fields = '__all__'


class SurveySerializer(serializers.ModelSerializer):
    question = QuestionSerializer(many=True)
    
    class Meta:
        model = Survey
        fields = '__all__'
    

class AnswerSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Answer
        fields = '__all__'
