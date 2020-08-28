from django.views import generic
from .models import Post
from django.urls import reverse_lazy

class IndexView(generic.ListView):
    template_name = 'home.html'
    context_object_name = 'post'
    def get_queryset(self): #ListView에서 사용-표시 하려는 개체 목록을 결정한다. 
        return Post.objects.all()

class DetailView(generic.DetailView):
    model = Post #queryset = Post.objects.all()이랑 같은 기능
    template_name = 'detail.html'
    context_object_name='ppost'

class DeleteView(generic.DeleteView):
    model = Post
    template_name = 'delete.html'
    context_object_name='ppost'
    success_url = reverse_lazy('home')

class UpdateView(generic.UpdateView):
    model = Post
    template_name = 'update.html'
    fields = ['title','content']
    success_url = reverse_lazy('home')