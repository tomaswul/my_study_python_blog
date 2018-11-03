"""__author__=wuliang"""
from django.shortcuts import render
from django.utils.deprecation import MiddlewareMixin


class ExceptionMiddleware(MiddlewareMixin):
	def process_exception(self, request, exception):
		return render(request, 'web/404.html', {'exception':exception})