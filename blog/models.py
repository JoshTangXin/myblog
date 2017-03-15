from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.urlresolvers import reverse
from time import strftime
from taggit.managers import TaggableManager


#默认的管理器是objects 现在我们需要自定义一个管理器 管理已经确认发布的帖子
class PublishedManager(models.Manager):
	def get_queryset(self):
		return super(PublishedManager,
					 self).get_queryset().filter(status='published')

# Create your models here.
class Post(models.Model):
	STATUS_CHOICES = (
		('draft','Draft'),
		('published','Published'),
	)
	# 博客的标题和主题内容 创建时间 更新时间 以及最终的发布时间等
	title = models.CharField(max_length=200)
	slug = models.SlugField(max_length=50, unique_for_date='publish_time')
	author = models.ForeignKey(User,related_name='blog_posts')
	body = models.TextField()
	create_time = models.DateTimeField(auto_now_add=True)
	update_time = models.DateTimeField(auto_now=True)
	publish_time = models.DateTimeField(default=timezone.now)

	# 帖子的状态
	status = models.CharField(max_length=10,choices=STATUS_CHOICES,default='draft')

	objects = models.Manager()	#默认管理器
	Published = PublishedManager()
	# taggit提供的标签管理器
	tags = TaggableManager()

	class Meta:
		ordering = ('-publish_time',)

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('blog:post_detail',args=[
			self.publish_time.year,
			self.publish_time.strftime('%m'),
			self.publish_time.strftime('%d'),
			self.slug])

class Comment(models.Model):
	post = models.ForeignKey(Post, related_name='comments')	#没有releated_name 智能通过_set来取所有值
	name = models.CharField(max_length=80)
	email = models.EmailField()
	body = models.TextField()
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	active = models.BooleanField(default=True)

	class Meta:
		ordering=('created',)

	def __str__(self):
		return 'Comment by {} on {}'.format(self.name, self.post)
