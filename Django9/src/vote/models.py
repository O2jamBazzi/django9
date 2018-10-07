from django.db import models
from django.contrib.auth.models import User

class Question(models.Model):
    name = models.CharField('질문내용',max_length=200)
    pub_date = models.DateTimeField('생성일')
    def __str__(self):
        return models.Model.__str__(self)
    
class Choice(models.Model):
    name = models.CharField('답변내용',max_length=100)
    vote = models.IntegerField('투표수',default=0)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    #연결된 Question객체가 지워질 경우 Choice 객체도 지워지도록 설정
    
#댓글을 저장하는 모델 클래스
#사용자, 댓글내용, 생성일
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.CharField('댓글내용',max_length=500)
    pub_date = models.DateTimeField('생성일',auto_now_add=True)