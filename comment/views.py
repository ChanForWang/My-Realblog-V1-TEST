from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Comment
from .forms import CommentForm


# Create your views here.
def upload_comment(request):
    referer = request.META.get('HTTP_REFERER', reverse('blog:index'))
    comment_form = CommentForm(request.POST, user=request.user)
    data = {}

    if comment_form.is_valid():
        # 数据检查通过，保存至数据库
        comment = Comment()
        comment.user = comment_form.cleaned_data['user']
        comment.comment_text = comment_form.cleaned_data['comment_text']
        comment.content_object = comment_form.cleaned_data['content_object']


        parent = comment_form.cleaned_data['parent']
        if not parent is None:
            comment.root = parent.root if not parent.root is None else parent
            comment.parent = parent
            comment.reply_to = parent.user
        comment.save()

        #返回数据
        data['status'] = 'SUCCESS'
        data['username'] = comment.user.username
        data['comment_time'] = comment.comment_time.strftime('%Y-%m-%d %H:%M:%S')
        data['comment_text'] = comment.comment_text
        if not parent is None:
            data['reply_to'] = comment.reply_to.username
        else:
            data['reply_to'] = ''
        data['pk'] = comment.id
        data['root_pk'] = comment.root.id if not comment.root is None else ''

    else:
        # message = comment_form.errors
        # redirect_to = referer
        # return render(request, 'error.html', locals())

        # 返回数据
        data['status'] = 'ERROR'
        data['message'] = list(comment_form.errors.values())[0][0]
    return JsonResponse(data)


