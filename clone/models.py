from django.db import models
from PIL import Image
from django.contrib.auth.models import User



# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(default='default.jpg', upload_to='profile_images')
    bio = models.TextField()

class Comment(models.Model):
    name= models.CharField(max_length=100, null=False, blank=False)
   
	
	
    def __str__(self):
        return self.name

  

class Photo (models.Model):
    comments = models.ForeignKey(Comment, on_delete=models.SET_NULL,null=True, blank=True)
    image=models.ImageField(null=False,blank=False,)
    description= models.TextField(max_length=500, null=False, blank=False)
    pub_date = models.DateTimeField(auto_now_add=True,null=True)

    def __str__(self):
        return self.description  


        