from django.contrib import admin

# Register your models here.
from .models import Post

admin.site.register(Post)

admin.site.site_header = '后台管理系统'
admin.site.site_title = '后台管理系统'