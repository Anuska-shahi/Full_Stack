from django.db import models
from account.models import CustomUser

# Create your models here.
class BlogPost(models.Model):
    title=models.CharField(max_length=50)
    content=models.TextField()
    published_date=models.DateTimeField(auto_now_add=True)
    deleted=models.BooleanField(default=False)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='blog_posts')

    def __str__(self):
        return self.title
    
    def delete(self ,hard_delete=False):
        if hard_delete:
                super().delete()
        else:
            self.deleted=True
            self.save()
    
    def restore(self):
        self.deleted=False
        self.save()