from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Categories(models.Model):
  name = models.CharField(max_length=30)
  
  class Meta:
    verbose_name_plural = "Categories"
  
  def __str__(self):
    return self.name
  
class Author(models.Model):
  user = models.ForeignKey(User,on_delete=models.CASCADE)
  bio = models.TextField(max_length=10000)
  profile_pic = models.ImageField(upload_to='authors/',blank=True,null=True)
  
  def __str__(self):
    return self.user.username
  
STATUS_CHOICE = (
  ('draft','draft'),
  ('posted','posted')
)

class Post(models.Model):
  title = models.CharField(max_length=50)
  slug = models.SlugField(unique=True)
  author_main = models.ForeignKey(Author, on_delete=models.CASCADE)
  blog_image = models.ImageField(upload_to='blogImage/',blank=True,null=True)
  body = models.TextField()
  short_description = models.TextField()
  conclusion = models.TextField()
  created_on = models.DateTimeField(auto_now_add=True)
  last_modified = models.DateTimeField(auto_now=True)
  categories = models.ForeignKey(Categories,on_delete=models.CASCADE)
  status = models.CharField(max_length=100,choices=STATUS_CHOICE,default='draft')
  
  def __str__(self):
    return self.title
  
 
  
class Comment(models.Model):
  author = models.ForeignKey(Author,on_delete=models.CASCADE)
  body = models.TextField(max_length=5000)
  created_on = models.DateTimeField(auto_now_add=True)
  post = models.ForeignKey(Post,on_delete=models.CASCADE)
  
  def __str__(self):
    return f"{self.author} on '{self.post}'"
  
