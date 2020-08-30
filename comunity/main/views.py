from django.shortcuts import render, redirect,get_object_or_404
from django.views import generic
from .models import Post, Comment
from .forms import CommentForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages

class IndexView(generic.ListView):
    template_name = 'home.html'
    context_object_name = 'post'
    def get_queryset(self): #ListView에서 사용-표시 하려는 개체 목록을 결정한다. 
        return Post.objects.all()

class DetailView(generic.DetailView):
    model = Post #queryset = Post.objects.all()이랑 같은 기능
    template_name = 'detail.html'
    context_object_name='ppost'
    
    ## template에 보낼 context 설정 : fbv에 {}로 담았던 context를 만드는 함수다.
    def get_context_data(self, **kwargs): 
        context_data = super(DetailView, self).get_context_data(**kwargs) #기본 context 인스턴스가 반환된다.
        context_data['form']=CommentForm()
        context_data['comments']=self.object.comment_set.all()
        return context_data
    
    ## 댓글 post 처리 후 할 행동 : 자동 새로고침 --> 댓글 post처리를 comment_create함수로 처리하기에 필요X
    # def get_sucess_url(self):
    #     return reverse('detail', kwargs={'pk':self.object.pk})
    
class UpdateView(generic.UpdateView):
    model=Post
    template_name = 'update.html'
    context_object_name='ppost'

    def get_context_data(self, **kwargs): 
        context_data = super(DetailView, self).get_context_data(**kwargs) #기본 context 인스턴스가 반환된다.
        context_data['form']=CommentForm()
        context_data['comments']=self.object.comment_set.all()
        return context_data
    

def comment_create(request, post_id):
    if not request.user.is_anonymous:
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.author=request.user
            comment.post_id=post_id
            comment.save()
        else:
            messages.info(request, "올바르지 않은 댓글입니다.")
    else:
        messages.info(request, "로그인이 필요합니다.")
    return HttpResponseRedirect(reverse('detail',args=(post_id,)))


def comment_update(request, post_id, comment_id):
    comment_value = Comment.objects.get(pk=comment_id)
    if comment_value.author == request.user:
        comment_form = CommentForm(instance=comment_value)
        if request.method == 'POST':
            updated_form=CommentForm(request.POST, instance=comment_value)
            if updated_form.is_valid():
                updated_form.save()
                return HttpResponseRedirect(reverse('detail',args=(post_id,)))
        return render(request,'update.html', {'comment_form':comment_form})
    else:
        messages.info(request,"댓글 수정 권한이 없습니다.")
        return HttpResponseRedirect(reverse('detail',args=(post_id,)))

def comment_delete(request, post_id ,comment_id):
    comment_value = Comment.objects.get(pk=comment_id)
    if comment_value.author == request.user:
        comment_value.delete()
        return HttpResponseRedirect(reverse('detail',args=(post_id,)))
    else:
        messages.info(request,"댓글 삭제 권한이 없습니다.")
        return HttpResponseRedirect(reverse('detail',args=(post_id,)))