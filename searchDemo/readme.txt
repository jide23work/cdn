
基本流程
前端使用Bootstrap构建搜索框；
搜索框输入关键词按下回车，关键词数据以表单形式发送至后台服务器；
服务器收到请求，通过路由url解析后找到对应的视图处理函数进行处理；
视图处理函数从request.get中获得关键词数据，然后通过数据库匹配查找对应的数据信息并返回结果；
前端收到返回的页面内容进行渲染；
详细开发步骤


1. 创建项目
打开VS Code或者cmd，在终端中输入命令：

django-admin startproject searchDemo
从而创建一个名为searchDemo的项目。用VS Code打开该文件夹，在该文件夹根目录下创建一个名为app的应用：

python manage.py startapp app
打开searchDemo子文件夹下的settings.py文件，修改ALLOWED_HOSTS字段：

ALLOWED_HOSTS = ['*',]
 

用于开放访问权限。然后在INSTALLED_APPS字段中添加刚创建的app应用：

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'app',  # 添加新创建的应用
]
 

保存修改后运行项目查看是否正常，在终端输入命令：

python manage.py runserver
下图即为项目创建正常显示图：



2. 开发前端首页
在app文件夹下创建一个模板文件夹templates，然后在templates文件夹下创建一个名为index.html的网页模板文件。下面从bootstrap官网找到模板代码（网址： https://v3.bootcss.com/getting-started/），将其复制到index.html中，略加修改部分内容，详细代码如下：

<!DOCTYPE html>
<html lang="zh-CN">
 
<head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>搜索框示例</title>
    <!-- Bootstrap -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@3.3.7/dist/css/bootstrap.min.css" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/jquery@1.12.4/dist/jquery.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@3.3.7/dist/js/bootstrap.min.js"></script>
</head>
 
<body>
    <div class="col-sm-4">
        <form method="get" action="/search/">
            {% csrf_token %}
            <div class="input-group">
                <input type="text" name="mykey" class="form-control" placeholder="请输入关键字" required />
                <span class="input-group-btn">
                    <input type="submit" class="btn btn-default" value="查询" />
                </span>
            </div>
        </form>
    </div>
</body>
 
</html>
上述代码在<body>标签中定义了一个bootstrap表单组件，该表单的请求方法为get，请求网址为"/search/"，在表单中包含一个搜索框控件。特别注意在 form 标签下有一个 {% csrf_token %}，这是 django 用来防御跨站请求伪造（CSRF）攻击的机制。如果没有这句代码，那么请求无法通过django服务器认证。

下面继续完善后端部分以渲染该网页。

3. 配置路由和视图响应函数
为了能够通过django显示刚才创建的首页，需要定义好首页路由以及对应的视图处理函数。打开app应用下的views.py文件，添加首页视图处理函数home，对应代码如下：

from django.shortcuts import render
 
# Create your views here.
def home(request):
    return render(request, 'index.html')
上述代码并不对请求进行解析，而是直接返回index.html文件给客户端浏览器。

接下来编写路由使得当前根网址(http://127.0.0.1:8000/)映射到home函数。打开searchDemo子文件夹下的urls.py文件，代码如下：

from django.conf.urls import url
from django.contrib import admin
 
from app.views import home
 
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    #添加首页路由
    url(r'^$', home, name='home'), 
]
保存修改后启动项目，浏览效果



4. 创建模型数据
为了完成搜索功能，需要创建一些模型数据以供匹配。下面以“文章”模型为例，建立相关的模型数据。

打开app文件夹下的models.py文件，编辑代码如下：

from django.db import models
 
# Create your models here.
class Post(models.Model):
    # 标题
    title = models.CharField(max_length=70)
    # 正文
    body = models.TextField()
 
    def __str__(self):
        return self.title
然后将该模型注册到后台管理系统中，打开admin.py文件，编辑代码如下：

from django.contrib import admin
 
# Register your models here.
from .models import Post
 
admin.site.register(Post)
 
admin.site.site_header = '后台管理系统'
admin.site.site_title = '后台管理系统'
完成模型定义后同步到数据库中，在终端中依次运行命令：

python manage.py makemigrations
python manage.py migrate
完成数据库同步。

最后，为了能够在后台管理系统中使用该模型，需要创建超级管理员账户。终端中输入命令：

python manage.py createsuperuser
然后按照提示输入姓名、邮箱、密码（其中密钥需要输入两遍以确认）。账户创建成功后运行项目然后登陆后台管理系统：

http://127.0.0.1:8000/admin

输入刚才创建的账户名和密码登陆到系统中。找到Posts模型，在该模型右侧单击Add按钮来添加数据，如下图所示：





数据填入完成后单击右侧SAVE按钮完成一条数据。按照这种方法添加多条数据以供后续搜索演示。

5. 模型数据搜索处理函数
本小节在后端视图函数中完成模型数据的搜索功能。编辑views.py文件，添加代码如下：

from .models import Post
 
def search(request):
    keyStr = request.GET.get('mykey')
    post_list = Post.objects.filter(title__icontains=keyStr)
    return render(request, 'result.html', {'post_list': post_list,})
首先使用 request.GET.get('keyStr') 获取到用户提交的搜索关键词。用户通过表单提交的数据 django 保存在request.GET 里，这是一个类似于 Python 字典的对象，所以可以使用 get 方法从字典里取出键 mykey对应的值，即用户的搜索关键词。这里字典的键之所以为mykey是因为我们的表单中搜索框 input 的 name 属性的值是 keyStr，如果修改了 name 属性的值，那么这个键的名称也要相应修改。如果用户输入了搜索关键词，就通过 filter 方法从数据库里过滤出符合条件的所有文章。这里的过滤条件是title__icontains=keyStr，即 title 中包含（contains）关键字 keyStr，前缀 i 表示不区分大小写。这里 icontains 是查询表达式，其用法是在模型需要筛选的属性后面跟上两个下划线。django 内置了很多查询表达式可供使用，具体请参考django官方文档。

在urls.py文件中添加search对应的路由：

from django.conf.urls import url
from django.contrib import admin
 
from app.views import home
from app.views import search
 
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    #添加首页路由
    url(r'^$', home, name='home'), 
    #搜索路由
    url(r'^search/$', search, name='search'),
]
6. 模型数据搜索处理函数
接下来就是渲染搜索结果页面，显示符合搜索条件的文章列表。在templates文件夹中新建一个名为result.html的模板文件，编辑代码如下：

{% load staticfiles %}
<!DOCTYPE html>
<html lang="zh-CN">
 
<head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>查询结果</title>
    <!-- Bootstrap -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@3.3.7/dist/css/bootstrap.min.css" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/jquery@1.12.4/dist/jquery.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@3.3.7/dist/js/bootstrap.min.js"></script>
</head>
 
<body>
 
    {% if post_list %}
        {% for post in post_list %}
            <h3>{{post.title}}</h3>
            <p>{{post.body}}</p>
        {% endfor %}
    {% else %}
        <h4>没有查询到数据</h4>
    {% endif %}
 
</body>
保存所有修改后运行项目，在输入框中输入“邮储”然后单击搜索，运行效果图如下所示：





至此已完成全部开发任务。全部代码下载地址：https://download.csdn.net/download/qianbin3200896/10997584

 

尾记
本文制作的django搜索功能是非常简略的，难以满足一些复杂的搜索需求。编写一个搜索引擎是一个大工程，如果需要实现诸如全文检索、按搜索相关度排序、关键字高亮等等复杂搜索功能推荐使用django-haystack 这款第三方app来完成工作。

 