from django.contrib import admin

from .models import post




@admin.register(post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title','slug','author','timeStamp','status')
    list_filter = ('status','timeStamp','author')
    search_fields = ('title','content')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)

    ordering = ('status','timeStamp')
# Register your models here.
