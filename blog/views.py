from django.shortcuts import render,get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin   #login in user can do something
from django.contrib.auth.models import User
from .models import post
from django.views.generic import (ListView,
                                  DetailView,
                                  CreateView,
                                  UpdateView,
                                  DeleteView)
from django.urls import reverse_lazy


def home(request):
    # context={'posts':posts}
    context = {'posts': post.objects.all()}
    return render(request,'blog/home.html',context)

class PostListView(ListView):
    model = post
    template_name = 'blog/home.html' # template_name = <app>/<model>_<view type>.html
    context_object_name = 'posts' #this will give posts to the home page
    ordering = ['-date_posted'] #newest to oldest post in home page
    paginate_by = 3

class UserPostListView(ListView):
    model = post
    template_name = 'blog/user_post.html' # template_name = <app>/<model>_<view type>.html
    context_object_name = 'posts' #this will give posts to the home page
    # ordering = ['-date_posted'] #newest to oldest post in home page
    paginate_by = 3

    def get_queryset(self):  #query_set has one word
        user = get_object_or_404(User,username = self.kwargs.get('username'))
        return post.objects.filter(author = user).order_by('-date_posted')


class PostDetailView(DetailView):
        model = post
        #create template by this naming convension (template_name = <app>/<model>_<view type>.html)

class PostCreateView(LoginRequiredMixin,CreateView):
    model = post
    fields = ['title','content']

    def form_valid(self, form):
        form.instance.author = self.request.user

        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = post
    fields = ['title','content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin ,DeleteView):
    model = post
    # success_url = '/'  #this will redirect to the location after delete
    success_url = reverse_lazy('Blog-home') #both work properly

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False




def about(request):
    return render(request,'blog/about.html',{'title':'About'})