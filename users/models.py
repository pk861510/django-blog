from django.db import models
from django.contrib.auth.models import User

from PIL import Image #resize Image


# Create your models here.
class profile(models.Model):
    user = models.OneToOneField(User,on_delete = models.CASCADE)  #if delete user then also delete profile
    image = models.ImageField(default = 'default.jpg',upload_to = 'profile_pics')
    about = models.CharField(max_length=400, null=True, blank=True)  # This is your custom field

    mfa_secret = models.CharField(max_length=32, blank=True, null=True)
    # Optional field to check if MFA is enabled
    mfa_enabled = models.BooleanField(default=False)
    
    def __str__(self):
        return f'{self.user.username} Profile'
    # Because now we use AWS S3 for our storages
    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)  #this args and kwargs important
    #     img = Image.open(self.image.path)
    #
    #     if img.height>300 or img.width>300:
    #         output_size = (300,300)
    #         img.thumbnail(output_size)
    #
    #         img.save(self.image.path)