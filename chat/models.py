from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

class User(AbstractUser):
    avatar_url = models.URLField(max_length=500, blank=True, null=True)
    is_online = models.BooleanField(default=False)
    
    def __str__(self):
        return self.username

class Friendship(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
    )
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friendships_initiated')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friendships_received')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user1', 'user2')

    def __str__(self):
        return f"{self.user1.username} - {self.user2.username} ({self.status})"

class Room(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, blank=True)
    host = models.ForeignKey(User, on_delete=models.CASCADE, related_name='hosted_rooms')
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_locked = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name or str(self.id)} (Host: {self.host.username})"

class Participant(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='participants')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='participated_rooms')
    joined_at = models.DateTimeField(auto_now_add=True)
    left_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} in {self.room.id}"
