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
            

class ApplyFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplyFile
        fields = '__all__'


class SurveySerializer(serializers.ModelSerializer):
    question = QuestionSerializer(many=True)
    
    class Meta:
        model = Survey
        fields = '__all__'
    

class AnswerSerializer(serializers.ModelSerializer):
    question = serializers.SerializerMethodField()
    
    class Meta:
        model = Answer
        fields = ['id', 'question', 'answer']
    
    def get_question(self, obj):
        return obj.question.content


class ApplierSerializer(serializers.ModelSerializer):
    answer = AnswerSerializer(many=True)
    applyfiles = ApplyFileSerializer(many=True)
    
    class Meta:
        model = Applier
        fields = '__all__'


class ApplierListSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Applier
        fields = ['id', 'name', 'birth', 'gender',\
            'phone', 'apply_date', 'is_favor', 'is_picked']