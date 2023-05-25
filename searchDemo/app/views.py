from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'index.html')


from .models import Post


def search(request):
    keyStr = request.GET.get('mykey')
    post_list = Post.objects.filter(title__icontains=keyStr)
    return render(request, 'index.html', {'post_list': post_list, })