# myblog
------

一个基于Django的个人博客

![myblog login](https://raw.githubusercontent.com/JoshTangXin/myblog/master/images/login.PNG)
------
![myblog](https://raw.githubusercontent.com/JoshTangXin/myblog/master/images/blog.PNG)

------
```
Note:You need django-debug-toolbar（pip install django-debug-toolbar）
And need add below in urls.py

if DEBUG:
    import debug_toolbar
    urlpatterns.append(url(r'^__debug__/', include(debug_toolbar.urls)))
```
