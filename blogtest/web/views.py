from django.db.models import Q
from django.shortcuts import render

# Create your views here.
from backweb.models import Article, ArticleClass


def index(request):
	if request.method == 'GET':
		cate_id = request.GET.get('cate_id')
		categorys = ArticleClass.objects.all()
		if not cate_id:
			arts = Article.objects.filter(status=0)
			return render(request,'web/index.html', {'arts':arts,'categorys':categorys})
		else:
			arts = ArticleClass.objects.get(pk=cate_id).article_set.filter(status=0)
			return render(request,'web/index.html', {'arts':arts,'categorys':categorys})
	if request.method == 'POST':
		categorys = ArticleClass.objects.all()
		keyboard = request.POST.get('keyboard')
		arts = Article.objects.filter(status=0).filter(Q(title__contains=keyboard)|
												Q(keyword__contains=keyboard)|
												Q(description__contains=keyboard))
		return render(request, 'web/index.html',{'arts':arts,'categorys':categorys})

def info(request, id):
	if request.method == 'GET':


		id = int(id)
		arts = Article.objects.filter(status=0)
		preart = arts.filter(id=(id-1)).first()
		nextart = arts.filter(id=(id+1)).first()
		art = arts.filter(id=id).first()
		art.count += 1
		art.save()

		categorys = ArticleClass.objects.all()

		return render(request, 'web/info.html', {'art': art,'categorys': categorys,
													   'preart':preart,'nextart':nextart})

