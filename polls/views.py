# polls/views.py
from django.http import HttpResponseRedirect      # !!!
from django.shortcuts import render, get_object_or_404
from django.urls import reverse                                 # !!!
# from django.http import Http404, HttpResponse,          # !!!
# from django.template import loader      # !!!
from .models import Question, Choice                            # !!!
from django.views import generic      # !!!


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """최근 게시된 투표 5개 반환"""
        return Question.objects.order_by('-pub_date')[:5]
# def index(request):
#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     context = {'latest_question_list': latest_question_list}
#     return render(request, 'polls/index.html', context)
# def index(request):
#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     template = loader.get_template('polls/index.html')
#     context = {
#         'latest_question_list': latest_question_list,
#     }
#     return HttpResponse(template.render(context, request))
# def index(request):
#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     output = ', '.join([q.question_text for q in latest_question_list])
#     return HttpResponse(output)
# def index(request):
#     return HttpResponse("여기는 투표 앱의 인덱스 페이지입니다.")


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'
# def detail(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/detail.html', {'question': question})
# def detail(request, question_id):
#     try:
#         question = Question.objects.get(pk=question_id)
#     except Question.DoesNotExist:
#         raise Http404("진행 중인 투표가 없습니다.")
#     return render(request, 'polls/detail.html', {'question': question})
# def detail(request, question_id):
#     return HttpResponse("%s번 투표 상세 보기" % question_id)


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'
# def results(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/results.html', {'question': question})
# def results(request, question_id):
#     response = "%s번 투표 결과 보기"
#     return HttpResponse(response % question_id)


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=int(request.POST['choice']))
    except (KeyError, Choice.DoesNotExist):
        # 투표 양식을 다시 출력
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "투표 항목을 선택하지 않았습니다.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # POST 데이터 처리가 성공하면, 항상 HttpResponseRedirect를 반환하라.
        # 이렇게 해야, 사용자가 돌아가기 버튼을 클릭해도 두번 게시되는 현상을 방지할 수 있다.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
# def vote(request, question_id):
#     return HttpResponse("%s번 투표에 반영 중..." % question_id)
