from django.shortcuts import render, get_object_or_404
from django.views import generic
from .models import Post, Comment
from .forms import CommentForm
from django.contrib.auth.mixins import LoginRequiredMixin

# ListView
class IndexView(generic.ListView):
    template_name = 'home.html'
    context_object_name = 'post'
    def get_queryset(self): #ListView에서 사용-표시 하려는 개체 목록을 결정한다. 
        return Post.objects.all()

class DetailView(generic.DetailView):
    model = Post #queryset = Post.objects.all()이랑 같은 기능
    template_name = 'detail.html'
    context_object_name='ppost'
    # comment_form = CommentForm()
    ## 댓글 post 처리 후 할 행동 -> 자동 새로고침
    def get_sucess_url(self):
        return reverse('detail', kwargs={'pk':self.object.pk})
    
    ## template에 보낼 context 설정
    def get_context_data(self, **kwargs): 
        #fbv에 {}로 담았던 context를 만드는 함수다.
        context_data = super().get_context_data(**kwargs) #기본 context 인스턴스가 반환된다.
        context_data['form']=CommentForm()
        return context_data