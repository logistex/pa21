# bookmark/views.py
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import render

from .models import Bookmark
from polls import models as polls_models
from photo import models as photo_models
from chart.views import covid_dump
# from chart.views import ticket_dump

def problems(request):
    return render(request, 'problems.html')


# class HomeView(DetailView):
#     pk = 1
#     model = polls_models.Question
#     template_name = 'home.html'
def home(request):
    question = polls_models.Question.objects.latest('id')
    bookmarks = Bookmark.objects.order_by('-id')[0:5]
    photos = photo_models.Photo.objects.all()[0:3]
    dump = covid_dump()
    # dump = ticket_dump()
    return render(request, 'home.html',
                  {'question': question, 'bookmarks': bookmarks, 'photos': photos,
                   'chart': dump,
                   }, )


class BookmarkListView(ListView):
    model = Bookmark
    paginate_by = 5  # 페이징 기능


class BookmarkCreateView(CreateView):
    model = Bookmark
    fields = ['site_name','url']
    success_url = reverse_lazy('bookmark:list')  # 글쓰기를 완료했을 때 이동할 페이지
    template_name_suffix = '_create'


class BookmarkDetailView(DetailView):
    model = Bookmark


class BookmarkUpdateView(UpdateView):
    model = Bookmark
    fields = ['site_name', 'url']
    template_name_suffix = '_update'  # 따라서 bookmark_update.html이어야 함
    success_url = reverse_lazy('bookmark:list')


class BookmarkDeleteView(DeleteView):
    model = Bookmark
    success_url = reverse_lazy('bookmark:list')


