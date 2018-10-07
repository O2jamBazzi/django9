from django.shortcuts import render, get_object_or_404
from vote.models import Question, Choice,Comment
from django.http.response import HttpResponseRedirect
#HttpResponseRedirect : HTML 파일을 클라이언트에게 보내주는것이 아닌,
#300번대 코드와 함께 URL주소를 클라이언트에게 전송함
from django.urls import reverse
from _datetime  import datetime
from idlelib.searchengine import get
#데코레이터 : 뷰함수 호출전 특정 조건을 만족하는지 검사하는 함수를 붙임
#요청자가 비로그인상태일때, 로그인페이지로 리다이렉트
from django.contrib.auth.decorators import login_required

def index(request):
    if request.method == 'GET':
        b = Comment.objects.all()   
        a = Question.objects.all()
        return render(request, 'vote/index.html',{'question_list' : a,'comment_list' : b })

    elif request.method=="POST":
        comment1 = request.POST.got('comment')
        obj = Comment()
        obj.comment = comment1
        obj.user = request.user
        obj.save()
        return HttpResponseRedirect(reverse('vote:index'))

#질문에 대한 설문지 제공
def detail (request, question_id):
    #get_object_or_404 : 모델클래스의 객체 한개를 추출, 조건에 맞는
    #객체가 없는경우 클라이언트에게 404 에러메시지를 전달
    question = get_object_or_404(Question, id = question_id)
    return render(request,'vote/detail.html', {'question' : question })
from django.db.models import F
#투표처리
def vote(request):
    #사용자가 POST 방식으로 요청했는지 확인
    if request.method == 'POST':
        id1 = request.POST.get('select')
        obj = get_object_or_404(Choice,id=id1)
        #obj.vote += 1 #객체 안에있는 vote 변수에 1증가
        obj.vote = F('vote')+1
        obj.save()
        # obj.question : question변수가 외되있래키로 저장으므로,
        # 연결된 객체를 저장함
        str(obj.question.id)
        return HttpResponseRedirect(reverse('vote:result',args=(obj.question.id, )))
#결과하면 보여주기
def result(request, question_id):
    obj = get_object_or_404(Question, id = question_id)
    
    return render(request, 'vote/result.html',{'question':obj})


from .forms import QuestionForm, ChoiceForm
#질문글 추가
def questionRegister(request):
    if request.method == "GET":
        form = QuestionForm() #QuestionForm 객체 생성
        print(form.as_table())
        return render(request, 'vote/questionRegister.html',{'form':form})
        
    #사용자 입력을 기반으로  Question 객체 생성 후 데이터베이스에 저장
    elif request.method == "POST":
        #사용자 입력을 해당 폼객체 생성시 넣을 수 있음
        form = QuestionForm(request.POST)
        #form.save() #사용자가 입력한 데이터를 데이터베이스에 저장
        #사용자가 입력한 데이터로 인증된 모델클래스의 객체로 변환
        obj = form.save(commit=False)
        obj.pub_date = datetime.now()
        obj.save()
        
        return HttpResponseRedirect( reverse('vote:index') )
#질문글 수정
def questionUpdate(request, question_id):
    obj = get_object_or_404(Question, id=question_id)
    if request.method == "GET":
        form = QuestionForm(instance = obj)
        
        return render(request,'vote/questionUpdate.html',{'form':form})
    elif request.method == "POST":
        #기존 객체를 사용자 입력 데이터로 변경
        form = QuestionForm(request.POST, instance = obj)  
        form.save() #데이터베이스에 변경사항 저장
        
        return HttpResponseRedirect(reverse('vote:index'))
#질문글 삭제
def questionDelete(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    question.delete()
    return HttpResponseRedirect(reverse('vote:index'))
    

#답변 추가
def choiceRegister(request):
    if request.method == "GET":
        obj = ChoiceForm()
        
        return render(request, 'vote/choiceRegister.html',{'form':obj})
    elif request.method == "POST":
        obj = ChoiceForm(request.POST)
        choice = obj.save()
        
        return HttpResponseRedirect(reverse('vote:index'))
        
    
    
    
#답변수정
def choiceUpdate(request, cid):
    
    obj = get_object_or_404(Choice, id = cid)
    
    if request.method == "GET":
        
        form = ChoiceForm(instance = obj)
        return render(request, 'vote/choiceUpdate.html',{'form':form, 'name' : '답변 수정 페이지', 'submit' : '답변 수정'})
        
    elif request.method == "POST":
        
        
        form = ChoiceForm(request.POST,instance=obj)
        form.save()
        return HttpResponseRedirect(reverse('vote:index'))
        
    
#답변삭제
def choiceDelete(request,choice_id):#1) 매개변수 추가
    #2) 삭제하고자 하는 객체를 찾기
    obj = get_object_or_404(Choice,id=choice_id); i = obj.question.id
    #3) delete함수 호출
    obj.delete()
    #4) 어딘가로 이동(index, detail)
    return HttpResponseRedirect(reverse('vote:index'))



