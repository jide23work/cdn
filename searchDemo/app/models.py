from django.db import models

# Create your models here.
class Post(models.Model):
    type = models.TextField()
    # 标题
    title = models.CharField(max_length=200)
    # 正文
    body = models.TextField()

    def __str__(self):
        return self.title