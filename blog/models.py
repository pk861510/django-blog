from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.
class post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User,on_delete = models.CASCADE)
    # prince = models.CharField(max_length=20)  #check after create a field prince in our database  and run migration commands

    def __str__(self):
        return self.title  # this is because if we write post.objects.all() it will return all the title of user
        return self.author

    def get_absolute_url(self):
        return reverse('Post-detail',kwargs={'pk': self.pk})  # - not post_detail right is Post-detail that we named our PostDetailView



