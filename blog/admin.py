from django.contrib import admin
from .models import Post,Comment

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
	list_display = ('title','slug','author','publish_time','status')
	list_filter = ('status', 'create_time', 'publish_time', 'author')
	search_fields = ('title', 'body')
	# 通过输入标题 自动补充slug
	prepopulated_fields = {'slug': ('title',)}
	#给author字段定义搜索控件 当作者比较多的时候 这个控件比较好用
	raw_id_fields = ('author',)
	ordering = ['status','publish_time']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'post', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('name', 'email', 'body')
# Register your models here.
#admin.site.register(Post)
