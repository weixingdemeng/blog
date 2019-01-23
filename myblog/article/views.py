from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from article.models import Article

from user.models import User


def article(request):
    if request.method == 'GET':
        articles = []
        article = Article.objects.all()
        num = len(article)
        username = request.session.get('username')
        user = User.objects.filter(u_name=username).first()
        for article1 in article:
            articles.append(article1)
            result = [user, articles, num]
        page = request.GET.get('page',1)
        pg = Paginator(article, 3)
        article = pg.page(page)

        # [user, [article1,....,articlen]]
        return render(request, 'article.html',{'article': article,'user':user, 'num':num})


def category(request):
    if request.method == 'GET':
        return render(request,'category.html')


def add_article(request):
    if request.method == 'GET':
        return render(request,'add-article.html')
    if request.method == 'POST':
        articles = []
        title = request.POST.get('title')
        content = request.POST.get('content')
        category = request.POST.get('category')
        tags = int(request.POST.get('tags'))
        titlepic = request.POST.get('titlepic')
        article = Article.objects.create(a_title=title,a_content=content,a_pre=category,a_category=tags)
        username = request.session.get('username')
        if not username:
            return HttpResponseRedirect(reverse('article:article'))
        articles.append(article)
        result = [username, articles]
        # request.session['article'] = article
        return render(request, 'add-article.html',{'result':result})


def change_article(request, id):
    if request.method == 'POST':
        articles = Article.objects.filter(id=id).first()
        return JsonResponse({'code':200, 'msg':'请求成功'})





def del_article(request, id):
    if request.method == 'POST':
        Article.objects.filter(id=id).delete()
        return JsonResponse({'code':200, 'msg':'请求成功'})


def update_article(request):
    if request.method == 'GET':
        return render(request, 'update-article.html')
