import uuid

from django.contrib.auth.models import User
from django.utils.text import slugify
from django.db import models


class Room(models.Model):
    owner    = models.ForeignKey(User, on_delete=models.CASCADE)
    members = models.ManyToManyField(User, related_name="member", blank=True)
    online   = models.BooleanField(default=True)
    name     = models.CharField(max_length=200)
    password = models.CharField(max_length=200, blank=True) 
    virtualId = models.CharField(max_length=200, blank=True)
    token    = models.CharField(max_length=100)
    slug     = models.SlugField()

    def token_code(self):
        token = str(uuid.uuid4())
        if Room.objects.filter(token=token).exists():
            self.token_code()
        return token

    def save(self, *args, **kwargs):
        self.slug  = slugify(self.name)
        self.token = self.token_code()
        self.virtualId = self.token_code()[:6]
        super(Room, self).save(*args, **kwargs)


class Message(models.Model):
    room   = models.ForeignKey(Room, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    text   = models.TextField()
    date   = models.DateTimeField(auto_now_add=True)
