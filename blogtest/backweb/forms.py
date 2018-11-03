"""__author__=wuliang"""
from django import forms
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User


class UserLoginForm(forms.Form):
	username = forms.CharField(max_length=10, min_length=2, required=True,
							   error_messages={
								   'max_length': '用户名不能超过10位',
								   'min_length': '用户名不能短于4位',
								   'required': '用户名不能为空',
							   })
	password = forms.CharField(max_length=16,min_length=6,required=True,
							   error_messages={
								   'max_length': '密码不能超过16位',
								   'min_length': '密码不能小于6位',
								   'required': '密码不能为空',
							   })


class ArticleForm(forms.Form):
	title = forms.CharField(max_length=20, required=True, error_messages={
		'max_length': '标题不能长度不能超过20个字符',
		'required': '标题不能为空'
	})

	content = forms.CharField(required=True,
							  error_messages={
								  'required': '内容不能为空'
							  }
							  )
	keywords = forms.CharField(max_length=20, error_messages={
		'max_length': '关键字不能超过20个'
	})

	describe = forms.CharField(max_length=150, min_length=10, required=True,
							   error_messages={
								   'max_length': '描述不能超过150字符',
								   'min_length': '描述不能少于10个字符',
								   'required': '描述不能为空'
							   })
	category = forms.CharField()


	visibility = forms.CharField()

class ArticleClassForm(forms.Form):
	name = forms.CharField(max_length=20,min_length=2,required=True,
						error_messages={
							'max_length': '名称不能超过10字符',
							'min_length': '名称不能少于2个字符',
							'required': '名称不能为空'
						}
						   )
	alias = forms.CharField(max_length=20,min_length=2,required=True,
						error_messages={
							'max_length': '别名不能超过10字符',
							'min_length': '别名不能少于2个字符',
							'required': '别名不能为空'
						}
						   )
	fid = forms.IntegerField()
	keywords = forms.CharField(
		max_length=30, min_length=2, required=True,
		error_messages={
			'max_length': '关键字不能超过25字符',
			'min_length': '关键字不能少于2个字符',
			'required': '关键字不能为空'}
	)

	describe = forms.CharField(max_length=150, min_length=10, required=True,
							   error_messages={
								   'max_length': '描述不能超过150字符',
								   'min_length': '描述不能少于10个字符',
								   'required': '描述不能为空'
							   })


class MessageForm(forms.Form):
	username = forms.CharField (max_length=10, min_length=2, required=True,
								error_messages={
									'max_length': '用户名不能超过10位',
									'min_length': '用户名不能短于4位',
									'required': '用户名不能为空',
								})
	old_password = forms.CharField(max_length=16, min_length=6, required=True,
								error_messages={
									'max_length': '密码不能超过16位',
									'min_length': '密码不能小于6位',
									'required': '密码不能为空',
								})
	password = forms.CharField (max_length=16, min_length=6, required=True,
								error_messages={
									'max_length': '密码不能超过16位',
									'min_length': '密码不能小于6位',
									'required': '密码不能为空',
								})
	new_password = forms.CharField (max_length=16, min_length=6, required=True,
								error_messages={
									'max_length': '密码不能超过16位',
									'min_length': '密码不能小于6位',
									'required': '密码不能为空',
								})
	def clean(self):
		flag = check_password(self.cleaned_data.get('old_password'),
					   User.objects.filter (username=self.cleaned_data.get ('username')).first().password)
		if not flag:
			raise forms.ValidationError({'password': '密码错误'})
		if self.cleaned_data.get('password') != self.cleaned_data.get('new_password'):
			raise forms.ValidationError({'new_password': '确认密码与新密码不一致'})
		return self.cleaned_data


