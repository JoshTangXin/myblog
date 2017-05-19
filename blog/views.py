from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from .models import *
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from django.views.generic import ListView
from .forms import EmailPostForm,CommentForm,BlogForm
from django.core.mail import send_mail
from taggit.models import Tag
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect,Http404 ,HttpResponse

# Create your views here.
# 需要在setting.py中设置LOGIN_URL
@login_required
def post_list(request,tag_slug=None):
	posts = Post.Published.filter(owner=request.user)
	tag=None

	total_posts = posts.count()
	# 实现标签系统 tag
	if tag_slug:
		tag=get_object_or_404(Tag,slug=tag_slug)
		posts=posts.filter(tags__in=[tag])

	#实现分页机制,比如一页最多显示5个topic
	paginator = Paginator(posts,3)
	page = request.GET.get('page')
	try:
		posts = paginator.page(page)
	except PageNotAnInteger:
		posts = paginator.page(1)
	except EmptyPage:
		posts = paginator.page(paginator.num_pages)

	context = {'posts':posts,'page':page,'tag':tag,'total_posts':total_posts}
	return render(request,'blog/list.html',context)

@login_required
def post_detail(request,year,month,day,post):
	post = get_object_or_404(Post,
							 slug=post,
							 status='published',
							 publish_time__year=year,
							 publish_time__month=month,
							 publish_time__day=day
							 )

	comments = post.comments.filter(active=True)

	if request.method != 'POST':
		comment_form=CommentForm()
	else:
		comment_form = CommentForm(data=request.POST)
		if comment_form.is_valid():
			new_comment = comment_form.save(commit=False)
			new_comment.post = post
			new_comment.save()

	# 通过标签获取标签类似的帖子
	post_tags_ids = post.tags.values_list('id', flat=True)
	similar_posts = Post.Published.filter(tags__in=post_tags_ids).exclude(id=post.id)
	similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags','-publish_time')[:4]

	context = {'post': post,'comments':comments,'comment_form':comment_form,'similar_posts':similar_posts}
	return render(request,'blog/details.html',context)

# 我们换着方法  基于类的方法实现视图 同时urls.py也需要修改
class PostListView(ListView):
	model = Post
	queryset = Post.Published.all()
	context_object_name = 'posts'
	paginate_by = 3
	template_name = 'blog/list.html'

# 可以通过邮件分享
@login_required
def post_share(request,post_id):
	post=get_object_or_404(Post,id=post_id,status='published')
	sent=False

	if request.method == 'POST':
		form = EmailPostForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			post_url = request.build_absolute_uri(post.get_absolute_url())
			subject = '{} ({}) recommends you reading "{}"'.format(cd['name'], cd['email'], post.title)
			message = 'Read "{}" at {}\n\n{}\'s comments: {}'.format(post.title, post_url, cd['name'], cd['comments'])
			# send_mail(subject, message, 'admin@myblog.com', [cd['to']])
			sent = True
	else:
		form = EmailPostForm()
	return render(request, 'blog/share.html', {'post': post, 'form': form, 'sent': sent})

@login_required
def new_blog(request):
#	post=Post.objects.get(id='author_id')
	if request.method != 'POST':
		form = BlogForm()
	else:
		form = BlogForm(request.POST)
		if form.is_valid():
			new_form = form.save(commit=False)
			new_form.owner=request.user
			new_form.author=request.user
			new_form.save()
			return HttpResponseRedirect(reverse('blog:post_list'))

	context={'form':form}
	return render(request, 'blog/new_blog.html',context)
