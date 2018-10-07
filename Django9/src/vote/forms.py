'''
Created on 2018. 9. 29.

@author: user
'''
from django.forms.models import ModelForm
from .models import *


#Question 모델클래스와 연동된 폼클래스 정의
class QuestionForm(ModelForm):
    class Meta:
        model = Question
        fields = ['name']
        
class ChoiceForm(ModelForm):
    def __init__(self, *args, **kwargs):
        #modelForm 클래스의 생성자를 호출
        super().__init__(*args, **kwargs)
        self.fields['question'].label = "설문지"
    
    
    
    
    
    
    
    
    class Meta: #name, question
        model = Choice
        exclude = ['vote']
        
        


