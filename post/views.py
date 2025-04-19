from django.shortcuts import render,get_object_or_404
from .models import Post,Categories,Comment

# Create your views here.
def homepage(request):
  return render(request,'first/index.html',{})

def post_content(request,slug):
    posts = get_object_or_404(Post,slug=slug)
    context = {
      'post':posts
    }
    
    return render(request,"blog/product.html",context)

def blog_detail(request,pk):
  posts = Post.objects.filter(pk=pk)
  comments = Comment.objects.filter(post=posts)
  context = {
    'posts':posts,
    'comments':comments
  }
  
  return render(request,"blog/detail.html",context)


def category_list(request,category):
  category_obj = get_object_or_404(Categories,name=category)
  posts = Post.objects.filter(categories = category_obj)
  context = {
    'posts':posts
  }
  
  return render(request,'blog/category.html',context)




