from django.contrib import admin
from .models import *
# Register your models here.

class Post_model(admin.ModelAdmin):
  list_display = ("id","created_on","title","categories","author_main","created_on","blog_image","status")
  prepopulated_fields = {'slug':('title',)}
  search_fields = ("id","title","categories__name")
  list_editable = ("title","categories",)
  
  

admin.site.register(Author)
admin.site.register(Categories)
admin.site.register(Post,Post_model)
admin.site.register(Comment)



