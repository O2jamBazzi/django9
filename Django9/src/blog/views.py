from django.shortcuts import render
from django.views.generic.list import ListView
from .models import Post
from django.views.generic.edit import FormView
from django.http.response import HttpResponseRedirect
from django.urls.base import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from blog.models import PostImage, PostFile
#제네릭뷰 : 창고에서 제공하는 여러가지 기능을 수행하는 뷰클래스
#class 뷰이름(제네릭스 상속):
#상속받은 제네릭뷰클래스의 변수/메소드를 수정해 사용
#단, 해당 제네릭뷰가 어떤 기능을 수해아는지 정확히 알아야함
#어떤 변수/메소드를 사용할 수 있는지 알아야함
#ListView : 특정 객체의 목록을 다루는 기능을 하는 뷰클래스
class Index(ListView):
    template_name = 'blog/index.html'
    
    model = Post
    
    context_object_name = 'post_list'
    
    paginate_by = 5
    
from django.views.generic.detail import DetailView
from .forms import PostForm
class Detail(DetailView):
    template_name = 'blog/detail.html'
    model = Post
    context_object_name = 'obj'
    
class PostRegister(FormView, LoginRequiredMixin):
    form_class= PostForm #폼클래스명
    template_name = 'blog/postRegister.html'
    context_object_name = 'form'
    #사용자가 POST방식으로 요청했을때 데이터 유효성을 검사한 뒤 호출되는 메소드
    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.author = self.request.user
        obj.save()
        #사용자가 지정요청한 이미지파일, 파일 객체 생성
        for f in self.request.FILES.getlist('images'):
            image = PostImage(post=obj,image=f)
            #image = PostImage()
            #image.post = obj
            #image.image = f
            image.save()
        #사용자가 준 파일 정보에서 'files' 라벨로 온 데이터를 추출
        for f in self.request.FILES.getlist('files'):
            file = PostFile(post=obj, file=f)
        #완성한 글의 url로 이동s
        return HttpResponseRedirect(reverse('blog:detail', args=(obj.id,)) )
#검색기능구현
def searchP(request):
    #웹요청으로 온 데이터는 무조건 문자열 처리가 됨
    q = request.GET.get('query','') # 'query'로 데이터가 안온경우, 빈문자열(' ')을 반환
    
    #q에 들어있는 문자열을 포함한 제목을 가진 Post 객체를 검색
    #contains 명령 : 해당 변수에 문자열안에 우변값이 포함되어있는지 확인
    list = Post.objects.filter(headline__contains=q)
    return render(request, 'blog/search.html', {'list':list})
    
    
    
    
    
    