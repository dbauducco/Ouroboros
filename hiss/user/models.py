from django.contrib.auth import models as auth_models
from django.db import models


class EmailUserManager(auth_models.UserManager):

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(email, password, **extra_fields)


class User(auth_models.AbstractUser):
    """
    Overrides the AbstractUser class to make the email field required, and the old Django fields not.
    """
    objects = EmailUserManager()

    # Set email to the primary lookup field
    email = models.EmailField(unique=True, null=False, blank=False)

    # Explicitly set the originally-required fields to not exist
    username = None
    first_name = None
    last_name = None

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
