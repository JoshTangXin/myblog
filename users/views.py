from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import logout , login , authenticate
from django.contrib.auth.forms import UserCreationForm

# Create your views here.
# 注销用户
def logout_view(request):
	logout(request)
	return HttpResponseRedirect(reverse('blog:post_list'))

def register(request):

	if request.method != 'POST':
		# 默认表单
		form=UserCreationForm()
	else:
		form = UserCreationForm(data=request.POST)
		if form.is_valid():
			new_user = form.save()
			#注册成功就让用户自动登录
			authenticate_user=authenticate(username = new_user.username,password = request.POST['password1'])
			login(request,authenticate_user)
			return HttpResponseRedirect(reverse('learning_logs:index'))

	context={'form':form}
	return render(request, 'users/register.html', context)