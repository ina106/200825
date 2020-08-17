from django.shortcuts import render, get_object_or_404
from django.views import generic
from .models import Post

# ListView
class IndexView(generic.ListView):
    template_name = 'home.html'
    context_object_name = 'post'
    def get_queryset(self):
        return Post.objects.all()

class DetailView(generic.DetailView):
    model = Post
    template_name = 'detail.html'