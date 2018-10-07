from django.db import models
from unittest.util import _MAX_LENGTH

# 모델 클래스 정의
# 모델(Model) : 데이터베이스에 데이터를 저장할 때, 어떠한 형식으로 저장할지
#               관리하는 부분
#
#
class BookMark(models.Model):
    #해당 모델 클래스에 저장할 값을 정의할 때, 클래스 내의 변수 정의
    #변수 정의시  xxxxField 클래스의 객체를 변수에 대입해 어떤 값을 저장할지
    #CharField() : 글자수 제한이 있는 문자열을 저장하는 공간 정의
    bookname = models.CharField(max_length=100)
    bookurl = models.URLField()
    def __str__(self):
        return self.bookname
    