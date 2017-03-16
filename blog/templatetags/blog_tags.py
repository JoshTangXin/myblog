"""
自定义自己的模板标签
simple_tag：处理数据并返回一个字符串（string）
inclusion_tag：处理数据并返回一个渲染过的模板（template）
assignment_tag：处理数据并在上下文（context）中放置一个变量（variable）
"""

from django import template
from ..models import Post
from django.db.models import Count
from django.utils.safestring import mark_safe
import markdown

register=template.Library()

@register.simple_tag
def total_posts():
	return Post.Published.count()

@register.inclusion_tag('blog/latest_posts.html')
def show_latest_posts(count=5):
    latest_posts = Post.Published.order_by('-publish_time')[:count]
    return {'latest_posts': latest_posts}

@register.assignment_tag
def get_most_commented_posts(count=5):
	return Post.Published.annotate(
		total_comments=Count('comments')
	).order_by('-total_comments')[:count]

@register.assignment_tag
def get_less_commented_posts(count=3):
    return Post.Published.annotate(total_comments=Count('comments')).order_by('total_comments')[:count]

# 自定义模板过滤器
@register.filter(name='markdown')
def markdown_format(text):
	return mark_safe(markdown.markdown(text))

