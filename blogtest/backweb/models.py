from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class ArticleClass(models.Model):
	classname = models.CharField(max_length=20)
	alias = models.CharField(max_length=20,null=True,unique=True)
	count = models.IntegerField(default=0)
	description = models.CharField (max_length=150, null=True)
	fatherid = models.IntegerField(default=0)
	keyword = models.CharField(max_length=30,null=True)
	user = models.ForeignKey(User)

	class Meta:
		db_table = 'tb_articleclass'




class Article(models.Model):
	title = models.CharField(max_length=32)
	description = models.CharField(max_length=255)
	content = models.TextField()
	create_time = models.DateTimeField(auto_now_add=True)
	update_time = models.DateTimeField(auto_now=True)
	status = models.BooleanField(default=True)
	keyword = models.CharField(max_length=20, null=True)
	count = models.IntegerField(default=0)
	img = models.ImageField(upload_to='article',null=True)
	articleclass = models.ForeignKey(ArticleClass)
	user = models.ForeignKey(User)

	class Meta:
		db_table = 'tb_article'

