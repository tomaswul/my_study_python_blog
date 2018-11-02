"""__author__=wuliang"""
from django.conf.urls import url

from web import views

urlpatterns = [
	url(r'^index/', views.index, name='index'),
	url(r'^info/(\d+)', views.info, name='info'),


]