from django.db import models
from django.contrib.auth.models import AbstractBaseUser, UserManager, PermissionsMixin
from django.utils import timezone

# Create your models here.
class MyUser(AbstractBaseUser, PermissionsMixin):
    # Basic information of user
    username = models.CharField(max_length=40, unique=True, blank=False)
    first_name = models.CharField(max_length=40, blank=False)
    last_name = models.CharField(max_length=40, blank=False)
    email = models.EmailField(blank=False)
    # The profile picture and the date of birth can be i=empty
    date_of_birth = models.DateField(null=True, blank=True)
    profle_pic = models.ImageField(null=True, blank=True)

    # Management variables for django
    is_staff = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    last_login = models.DateTimeField(default=timezone.now)
    date_joined = models.DateTimeField(default=timezone.now)

    # The manager to control the objects created using this model
    objects = UserManager()
    # The identifier of this model in the database, using username for simplicity
    USERNAME_FIELD = "username"
    EMAIL_FIELD = "email"
    # Must-have information when creating an account
    REQUIRED_FIELDS = ["first_name", "last_name", "email"]

    # Override these methods when needed, but extending PermissionsMixin is enough
    #
    # def has_perm(self, perm, obj=None):
    #     "Does the user have a specific permission?"
    #     # Simplest possible answer: Yes, always
    #     return True
    #
    # def has_module_perms(self, app_label):
    #     "Does the user have permissions to view the app `app_label`?"
    #     # Simplest possible answer: Yes, always
    #     return True

    def __str__(self):
        return self.first_name + " " + self.last_name
