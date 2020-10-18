from django.db import models
from UserRole.models import ContentType

# Create your models here.

class Blog(models.Model):
    title = models.CharField(max_length=250)
    type_id = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="blog_image")
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title