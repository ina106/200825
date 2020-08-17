from django.shortcuts import render, redirect,get_object_or_404
from django.views import generic
from .models import Post, Comment
from .forms import CommentForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages

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
        context_data = super(DetailView, self).get_context_data(**kwargs) #기본 context 인스턴스가 반환된다.
        context_data['form']=CommentForm()
        context_data['comments']=self.object.comment_set.all()
        return context_data

def comment_create(request, post_id):
    # post_obj = get_object_or_404(Post, pk=post_id)
    if not request.user.is_anonymous:
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.author=request.user
            comment.post_id=post_id
            comment.save()
        else:
            messages.info(request, "댓글 작성 실패")
            print("댓글작성 실패")
    else:
        messages.warning(request,"로그인 필요")
    return HttpResponseRedirect(reverse('detail',args=(post_id,)))
    # def form_valid(self, form):
    #     comment = form.save(commit=False)
    #     comment.author=self.request.user
    #     comment.content=
    # ## post요청이 들어왔을 때!(=댓글 생성하고 싶을 때)
    # def post(self, request, *args, **kwargs):
    #     self.object = self.get_object()
    #     form = self.get_form()

    #     if form.is_valid():
    #         return self.form_valid(form)
    #     else:
    #         return self.form_invalid(form) 
