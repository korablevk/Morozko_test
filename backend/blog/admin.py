from django.contrib import admin
from .models import Blogs
from django.forms import CheckboxSelectMultiple

class BlogsAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('title', 'description', 'slug')
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('products',)  

    exclude = ('created_at', 'updated_at')


admin.site.register(Blogs, BlogsAdmin)

