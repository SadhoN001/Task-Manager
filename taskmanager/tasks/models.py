from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Task(models.Model):
    STATUS = [ 
        ('pending', 'Pending'), 
        ('in_progress', 'In Progress'), 
        ('complete', 'Completed'), 
    ]
    PRIORITY =[
        ('low', 'Low'), 
        ('medium', 'Medium'), 
        ('high', 'High'), 
    ]

    title = models.CharField(max_length=100)
    description = models.TextField()
    status = models.CharField(max_length= 20, choices= STATUS, default= 'pending')
    priority = models.CharField(max_length= 10, choices= PRIORITY)
    created_at = models.DateTimeField(auto_now_add= True)
    updated_at  = models.DateTimeField(auto_now= True)
    due_date = models.DateField()
    owner = models.ForeignKey(User, on_delete= models.CASCADE)
    
    def __str__(self):
        return self.title
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    phone = models.CharField(max_length=15, blank=True)
    avatar = models.ImageField(upload_to="avatar/", blank= True, null=True)
    birth_date = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=100, blank=True)
    website = models.URLField(blank=True)
    
    def __str__(self):
        return self.user.username
    