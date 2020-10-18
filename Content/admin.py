from django.contrib import admin
from Content.models import Blog

# Register your models here.

class BlogAdmin(admin.ModelAdmin):
    list_display = ('title','image','description','created_at')
admin.site.register(Blog, BlogAdmin)