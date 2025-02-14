from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from datetime import timedelta
from django.utils import timezone

class CustomUser(AbstractUser):
    PHONE_NUMBER = 'phone_number'
    MEMBERSHIP_CHOICES = [
        ('silver', 'Silver'),
        ('gold', 'Gold'),
        ('diamond', 'Diamond'),
    ]
    
    phone_number = models.CharField(max_length=15, unique=True)
    membership_type = models.CharField(max_length=10, choices=MEMBERSHIP_CHOICES, default='silver')
    membership_start_date = models.DateField(default=timezone.now)
    membership_expiry_date = models.DateField()

    groups = models.ManyToManyField(
        Group,
        related_name='customuser_set',  
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_set',  
        blank=True
    )

    def save(self, *args, **kwargs):
        if not self.membership_expiry_date:
            if self.membership_type == 'silver':
                self.membership_expiry_date = self.membership_start_date + timedelta(days=365)
            elif self.membership_type == 'gold':
                self.membership_expiry_date = self.membership_start_date + timedelta(days=730)
            elif self.membership_type == 'diamond':
                self.membership_expiry_date = self.membership_start_date + timedelta(days=1095)
        super().save(*args, **kwargs)
