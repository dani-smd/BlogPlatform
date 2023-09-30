from django.db import models
from django.contrib.auth.models import AbstractUser

Gender = (
    ("ML", "Male"),
    ("FL", "Female"),
)


class User(AbstractUser):
    user_image = models.FileField(upload_to=f'uploads/user_images/%Y/%m/%d/', null=True,
                                  blank=True)
    phone_number = models.BigIntegerField(verbose_name="Phone Number", null=True, blank=True)
    gender = models.CharField(max_length=2, choices=Gender, verbose_name="Gender", null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name="Creation Date&Time")

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.username
