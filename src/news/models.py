from django.db import models

# Create your models here.

class newsBit(models.Model):
    title = models.CharField(max_length=200)
    channel= models.CharField(max_length=50)
    transcript = models.TextField()
    category= models.CharField(max_length=50)
    publication_date = models.DateTimeField()
    video_url = models.URLField()
    image = models.URLField()
    guid = models.CharField(max_length=50)
    summary = models.TextField(blank=True, null=True)
    
    def __str__(self) -> str:
        return f"{self.category}: {self.title}: {self.channel}"