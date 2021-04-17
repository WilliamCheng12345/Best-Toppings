from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from posts.models import Post, Comment
from django.core.exceptions import PermissionDenied


# Create your views here.
class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'sign_up.html'


def renderAccountView(request):
    if request.user.is_authenticated:
        logged_in_user_posts = Post.objects.filter(author=request.user)
        logged_in_user_comments = Comment.objects.filter(author=request.user)
        return render(request, 'account.html', {'posts': logged_in_user_posts, 'comments': logged_in_user_comments})
    else:
        raise PermissionDenied
