

# models.py
from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    hostel_block = models.CharField(max_length=10, choices=[
        ('A', 'Block A'),
        ('B', 'Block B'),
        ('C', 'Block C'),
        ('D', 'Block D'),
    ])
    phone_number = models.CharField(max_length=15, blank=True, null=True)

class UserLoginLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    login_time = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True)

class Issue(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=[
        ('Maintenance', 'Maintenance'),
        ('Electrical', 'Electrical'),
        ('Plumbing', 'Plumbing'),
        ('Other', 'Other'),
    ])
    location = models.CharField(max_length=100)
    reported_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Resolved', 'Resolved'),
    ], default='Pending')

# Ise view mein login() success hone ke baad save karein.