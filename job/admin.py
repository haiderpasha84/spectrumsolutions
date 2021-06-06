from django.contrib import admin
from .models import StudentUser
from .models import Recruiter,Apply,Catagory,Add_job
# Register your models here.


class jobAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')

class catAdmin(admin.ModelAdmin):
    list_display = ('id', 'catagory_name')

admin.site.register(StudentUser)
admin.site.register(Recruiter)
admin.site.register(Add_job , jobAdmin)
admin.site.register(Apply)
admin.site.register(Catagory ,catAdmin)
