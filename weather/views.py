from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
import requests
import re
import json
import os
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Post
from users.models import Profile
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from WeatherApp import settings
from django.contrib.auth.models import User


class MainPageListView(ListView):
    model = Post
    context_object_name = 'posts'
    queryset = Post.objects.order_by('-date_posted')[:2]


class PostListView(ListView):
    model = Post
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 30


class UserPostListView(ListView):
    model = Post
    context_object_name = 'posts'
    paginate_by = 30

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class ProfilePostListView(ListView):
    model = Post
    context_object_name = 'posts'
    paginate_by = 30

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']
    login_url = '/login/'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']
    login_url = '/login/'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def index(request):
    if request.POST:
        city = request.POST['citynameinput']

        appid = os.environ['appid']
        flickr_api = os.environ['flickr_api']
        yandex_api = os.environ['yandex_api']

        url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=' + appid

        list_of_pictures = 'https://www.flickr.com/services/rest/?method=flickr.photos.search&api_key={}&tags={}&text={}_city&media=photos&format=json&nojsoncallback=1&'
        get_list_of_pictures = requests.get(
            list_of_pictures.format(flickr_api, city, city)).json()
        list_of_urls = 'https://www.flickr.com/services/rest/?method=flickr.photos.getSizes&api_key={}&photo_id={}&format=json&nojsoncallback=1'

        pictures_url = []
        try:
            for i in range(5):
                id = get_list_of_pictures['photos']['photo'][i]['id']
                url_id = requests.get(
                    list_of_urls.format(flickr_api, id)).json()
                pictures_url.append(url_id['sizes']['size'][3]['source'])
        except IndexError:
            pass
        yandex_url_def = 'https://translate.yandex.net/api/v1.5/tr.json/detect?key=' + \
            yandex_api + '&text=' + city

        yandex_res = requests.get(yandex_url_def).json()

        if yandex_res['lang'] != 'en':
            yandex_url_translate = 'https://translate.yandex.net/api/v1.5/tr.json/translate?key=' + \
                yandex_api + '&text=' + city + '&lang=en'
            yandex_city = requests.get(yandex_url_translate).json()
            city = yandex_city['text'][0]

        res = requests.get(url.format(city)).json()

        yandex_url_translate = 'https://translate.yandex.net/api/v1.5/tr.json/translate?key=' + \
            yandex_api + '&text=' + city + '&lang=ru'
        yandex_city = requests.get(yandex_url_translate).json()
        city = yandex_city['text'][0]

        try:
            city_info = {
                'pressure': res['main']['pressure'],
                'wind_speed': res['wind']['speed'],
                'temp_min': round(int(res['main']['temp_min'])),
                'temp_max': round(int(res['main']['temp_max'])),
                'name': city,
                'temp': round(int(res['main']['temp'])),
                'country': res['sys']['country'],
                'icon': res['weather'][0]['icon'],
            }
        except KeyError:
            return render(request, 'error_page.html')
        else:
            context = {'info': city_info,
                       'picture': pictures_url}

        return render(request, 'results.html', context)
