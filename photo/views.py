# from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy
from .models import Photo


# @login_required
# def photo_list(request):
#     photos = Photo.objects.all()
#     return render(request, 'photo/list.html', {'photos': photos})
class PhotoListView(LoginRequiredMixin, ListView):
    model = Photo
    paginate_by = 3
    template_name = 'photo/list.html'


class PhotoUploadView(LoginRequiredMixin, CreateView):
    model = Photo
    fields = ['photo', 'text']
    template_name = 'photo/upload.html'

    def form_valid(self, form):
        # 로그인한 사용자 id를 다시 입력 요구하지 말도록
        form.instance.author_id = self.request.user.id
        if form.is_valid():
            form.instance.save()
            # return redirect('/')
            return redirect('photo:photo_list')
        else:
            return self.render_to_response({'form': form})


class PhotoDeleteView(LoginRequiredMixin, DeleteView):
    model = Photo
    # success_url = '/'
    success_url = reverse_lazy('photo:photo_list')
    template_name = 'photo/delete.html'


class PhotoUpdateView(LoginRequiredMixin, UpdateView):
    model = Photo
    fields = ['photo', 'text']
    template_name = 'photo/update.html'


class PhotoDetailView(LoginRequiredMixin, DetailView):
    model = Photo
    template_name = 'photo/detail.html'
