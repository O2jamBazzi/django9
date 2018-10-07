from django.db import models
from django.conf import settings
#카테고리

class PostType(models.Model):
    name = models.CharField('카테고리',max_length = 100)
    def __str__(self):
        return self.name
#글(글 제목, 글내용, 작성자, 작성일, 카테고리(외래키) )
class Post(models.Model):
    type  = models.ForeignKey(PostType,on_delete=models.PROTECT)
    headline = models.CharField('제목',max_length = 200)
    
    content = models.TextField('내용')
    
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    pub_date = models.DateTimeField('작성일',auto_now_add=True)

    class Meta: #모델 클래스도  Meta 클래스를 정의해서 추가적인 정렬, 정보를 제공
        ordering = ['-id']
        verbose_name = '글'
#이미지 저장
class PostImage(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    #Image Field() : 이미지를 저장하는 필드
    #upload_to : 이미지 저장시 어떤 폴더이름으로 분류할지 지정하는 매개변수
    image = models.ImageField('이미지파일', upload_to = "images/%Y/%m/%d")
    def delete(self, using=None, keep_parents=False):
        self.image.delete()
        return models.Model.delete(self, using=using, keep_parents=keep_parents)
    
    
    

    
#파일 저장
class PostFile(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    file = models.FileField('파일', upload_to = 'files/%Y/%m/%d')