from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.conf import settings

import os


def user_directory_path(instance, filename):
    return os.path.join('image/profile/', instance.user.username, filename)


class OverwriteStorage(FileSystemStorage):
    def get_available_name(self, name, max_length):
        if self.exists(name):
            os.remove(os.path.join(settings.MEDIA_ROOT, name))
        return name


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user')
    nickname = models.CharField(max_length=30, default=None, null=True,blank=True)
    avatar = models.ImageField(storage=OverwriteStorage(), upload_to=user_directory_path, null=True, blank=True)

    def __str__(self):
        return f'{self.nickname} '


class Chat(models.Model):
    title = models.CharField(max_length=128)
    members = models.ManyToManyField(Customer, through='ChatCustomer', related_name='rooms')

    def get_absolute_url(self):
         return reverse('chat', args=[str(self.id)])

    @property
    def members_list(self):
        return [m.id for m in self.members.all()]

    def __str__(self):
        members_line = [m.id for m in self.members.all()]
        return f'{self.title} {members_line}'


class ChatCustomer(models.Model):
    customers = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='customers')
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='chat')


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    time_in = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return f'from:{self.sender.id} to_chat:{self.chat.id} [{self.text[:50]}'





