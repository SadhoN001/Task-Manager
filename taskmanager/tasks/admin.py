from django.contrib import admin
from .models import Task, User, Profile

# Register your models here.
class TaskAdmin(admin.ModelAdmin):
    list_display=('id','title','description',"status", "priority", "due_date", "owner","created_at", "updated_at")
    
admin.site.register(Task, TaskAdmin)

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'location']
    
admin.site.register(Profile, ProfileAdmin)