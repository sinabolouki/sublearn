from django.db import models
from django.contrib.auth.models import User
from PIL import Image


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    image = models.ImageField(default='default.jpeg', upload_to='profile_pics')
    quiz_score = models.FloatField(null=True, blank=True)
    premium_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} Profile"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size =  (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

class EmailCode(models.Model):
    email = models.EmailField()
    code = models.IntegerField()
    date_changed = models.DateTimeField(auto_now=True)

