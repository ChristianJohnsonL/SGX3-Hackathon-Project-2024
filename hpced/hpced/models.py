from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import AbstractUser



class CustomUser(AbstractUser):
    search_resource_server = models.CharField(max_length=255, null=True)
    search_access_token = models.CharField(max_length=255, null=True)
    search_refresh_token = models.CharField(max_length=255, null=True, blank=True)
    search_expires_at = models.DateTimeField(null=True)
    search_scope = models.CharField(max_length=255, null=True)

    
# class GlobusToken(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
#     provider = models.CharField(max_length=255)
#     resource_server = models.CharField(max_length=255)
#     access_token = models.CharField(max_length=255)
#     refresh_token = models.CharField(max_length=255, null=True, blank=True)
#     expires_at = models.DateTimeField()
#     scope = models.CharField(max_length=255)

#     def __str__(self):
#         return f"{self.user} - {self.resource_server}"

    