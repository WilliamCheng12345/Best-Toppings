from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Post, Comment


# Create your views here.
class PostsListView(ListView):
    model = Post
    template_name = 'posts_list.html'


class PostsDetailView(DetailView):
    model = Post
    template_name = 'posts_detail.html'


class PostsCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'posts_new.html'
    fields = ['title', 'meat', 'non_meat', 'body']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostsEditView(UserPassesTestMixin, UpdateView):
    model = Post
    template_name = 'posts_edit.html'
    fields = ['title', 'meat', 'non_meat', 'body']

    def test_func(self):
        post_author = self.get_object().author
        return post_author == self.request.user


class PostsDeleteView(UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'posts_delete.html'
    success_url = reverse_lazy('account')

    def test_func(self):
        post_author = self.get_object().author
        return post_author == self.request.user


class CommentsCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    template_name = 'comments_new.html'
    fields = ['comment']

    def form_valid(self, form):
        comment_post = Post.objects.get(pk=self.kwargs['pk'])
        form.instance.author = self.request.user
        form.instance.post = comment_post
        return super().form_valid(form)


class CommentsDeleteView(UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'comments_delete.html'

    def get_success_url(self):
        post = self.get_object().post
        return reverse_lazy('posts_detail', kwargs={'pk': post.pk})

    def test_func(self):
        comment_author = self.get_object().author
        return comment_author == self.request.user


class CommentsEditView(UserPassesTestMixin, UpdateView):
    model = Comment
    template_name = 'comments_edit.html'
    fields = ['comment']

    def test_func(self):
        comment_author = self.get_object().author
        return comment_author == self.request.user
