import json

from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.core.paginator import Paginator

from django.urls import reverse

from backweb.forms import UserLoginForm, ArticleForm, ArticleClassForm, MessageForm
from backweb.models import Article, ArticleClass


def login(request):
	if request.method == 'GET':
		return render(request, 'backweb/login.html')
	if request.method == 'POST':
		data = request.POST
		form = UserLoginForm(data)
		if not form.is_valid():
			return render(request, 'backweb/login.html', {'error': form.errors})
		user = auth.authenticate(username=form.cleaned_data.get('username'),
								 password=form.cleaned_data.get('password'))
		if not user:
			return render(request, 'backweb/login.html', {'msg': '密码错误'})
		auth.login(request,user)

		return HttpResponseRedirect(reverse('backweb:index'))


@login_required
def index(request):
	if request.method == 'GET':
		count = Article.objects.count()
		all_count = 0
		for art in Article.objects.filter(count__gt=0):
			all_count += art.count
		return render(request, 'backweb/index.html',{'count': count,
													 'all_count': all_count})

	if request.method == 'POST':
		pass

@login_required
def article(request):
	if request.method == 'GET':
		# 展示文章实现分页
		articles = Article.objects.filter(Q(status=0)|Q(status=1))
		paginator = Paginator(articles, 6)
		page = request.GET.get('page')
		if page:
			arts = paginator.page(page)
		else:
			page = 1
			arts = paginator.page(page)

		return render(request, 'backweb/article.html', {'arts': arts, 'page': page})




@login_required
def add_article(request):
	if request.method == 'GET':
		categorys = ArticleClass.objects.all()
		return render(request, 'backweb/add-article.html', {'categorys':categorys})

	if request.method == 'POST':
		form = ArticleForm(request.POST)
		articleclass = ArticleClass.objects.get(id=form.data.get('category'))
		if form.is_valid():
			Article.objects.create(

				title=form.cleaned_data.get('title'),
				description=form.cleaned_data.get('describe'),
				content=form.cleaned_data.get('content'),
				keyword=form.cleaned_data.get('keywords'),
				articleclass=articleclass,
				img=request.FILES.get('titlepic'),
				status=form.cleaned_data.get('visibility'),
				user=request.user,


			)
			articleclass.count += 1
			articleclass.save()

			return HttpResponseRedirect(reverse('backweb:article'))
		return render(request, 'backweb/add-article.html',{'error': form.errors})


@login_required
def add_category(request):
	if request.method == 'GET':
		categorys = ArticleClass.objects.all()
		return render(request, 'backweb/category.html',{'categorys': categorys})
	if request.method == 'POST':
		form = ArticleClassForm(request.POST)
		categorys = ArticleClass.objects.all()
		if form.is_valid():

			ArticleClass.objects.create(
				classname=form.cleaned_data.get('name'),
				alias=form.cleaned_data.get('alias'),
				keyword=form.cleaned_data.get('keywords'),
				description=form.cleaned_data.get('describe'),
				fatherid=form.cleaned_data.get('fid'),
				user=request.user
			)
			return HttpResponseRedirect(reverse('backweb:add_category'))
		else:
			return render(request, 'backweb/category.html', {'error':form.errors,'categorys':categorys})

@login_required
def update_category(request,id):
	if request.method == 'GET':
		categorys = ArticleClass.objects.all()
		category = ArticleClass.objects.get(pk=id)
		return render(request, 'backweb/update-category.html', {'category':category,'categorys':categorys})

	if request.method == 'POST':
		form = ArticleClassForm(request.POST)
		categorys = ArticleClass.objects.all()
		category = ArticleClass.objects.get(pk=id)
		if form.is_valid():
			category.classname = form.cleaned_data.get('name')
			category.user = request.user
			category.alias = form.cleaned_data.get('alias')
			category.keyword = form.cleaned_data.get('keywords')
			category.description = form.cleaned_data.get('describe')
			category.fatherid = form.cleaned_data.get ('fid')

			category.save()

			return HttpResponseRedirect(reverse('backweb:add_category'))

		else:
			return render(request, 'backweb/update-category.html', {'error':form.errors,
																	'category':category,
																	'categorys':categorys})

@login_required
def delete_category(request):
	if request.method == 'POST':
		id = request.POST.get('id')
		articleclass = ArticleClass.objects.get(pk=id)
		articleclass.article_set.all().delete()
		articleclass.delete()

		categorys = ArticleClass.objects.all()

		return HttpResponse('成功')


def update_article(request, id):
	if request.method == 'GET':
		art = Article.objects.get(pk=id)
		categorys = ArticleClass.objects.all()

		return render(request, 'backweb/update-article.html', {'art':art, 'categorys':categorys})

	if request.method == 'POST':
		form = ArticleForm(request.POST)
		if form.is_valid():

			article = Article.objects.get(pk=id)
			# 减掉原来栏目的文章数量一个
			article.articleclass.count -= 1
			article.save ()

			article.articleclass = ArticleClass.objects.get(id=form.cleaned_data.get('category'))
			# 增加新栏目的文章数量一个
			article.articleclass.count += 1


			article.user = request.user
			article.keyword = form.cleaned_data.get('keywords')
			article.title = form.cleaned_data.get ('title')
			article.description = form.cleaned_data.get ('describe')
			article.content = form.cleaned_data.get ('content')
			article.img = request.FILES.get ('titlepic')
			article.status = form.cleaned_data.get ('visibility')
			article.save()

			return HttpResponseRedirect(reverse('backweb:article'))


def delete_article(request):
	if request.method == 'GET':
		return HttpResponseRedirect(reverse('backweb:article'))
	if request.method == 'POST':
		article = Article.objects.get(pk=request.POST.get('id'))
		if article.articleclass.count>0:
			article.articleclass.count -= 1
		article.status = 2
		article.save()

		return HttpResponse('删除成功')

@login_required
def logout(request):
	if request.method == 'GET':
		auth.logout(request)
		return HttpResponseRedirect(reverse('backweb:login'))

def search(request):
	if request.method == 'POST':
		# 展示文章实现分页
		keys = request.POST.get('keys')
		articles = Article.objects.filter (Q (status=0) | Q (status=1))\
			.filter(Q(title__contains=keys)|
					Q(keyword__contains=keys)|
					Q(description__contains=keys))

		paginator = Paginator (articles, 6)
		page = request.POST.get ('n_page')
		if page:
			arts = paginator.page (page)
		else:
			page = 1
			arts = paginator.page (page)

		return render (request, 'backweb/article.html', {'arts': arts, 'page': page})


@login_required
def alter_message(request):
	if request.method == 'GET':
		return render(request, 'backweb/change_message.html')
	if request.method == 'POST':
		form = MessageForm(request.POST)

		if form.is_valid():
			user = User.objects.get(pk=request.user.id)
			user.clean()

			user.username = form.cleaned_data.get('username')
			user.password = make_password(form.cleaned_data.get('password'))
			user.save()
			return HttpResponseRedirect(reverse('backweb:login'))
		return render(request,'backweb/change_message.html',{'error':form.errors})


