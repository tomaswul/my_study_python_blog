"""__author__=wuliang"""
from django.conf.urls import url

from backweb import views

urlpatterns = [
	url(r'^login/', views.login, name='login'),
	url(r'^index/', views.index, name='index'),
	url(r'^article/', views.article, name='article'),
	url(r'^add_article/', views.add_article, name='add_article'),
	url(r'^add_category/', views.add_category, name= 'add_category'),
	url(r'^update_category/(\d+)', views.update_category, name='update_category'),
	url(r'^delete_category/', views.delete_category,name='delete_category'),

	url(r'^update_article/(\d+)', views.update_article, name='update_article'),
	url(r'^delete_article/', views.delete_article, name='delete_article'),
	url(r'^logout/', views.logout, name='logout'),
	url(r'^search/', views.search, name='search'),
]