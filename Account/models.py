from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)


# Create your models here.
from rest_framework.permissions import IsAuthenticated

from UserRole.models import Role


class MyUserManager(BaseUserManager):
    def create_user(self, first_name, last_name, mobile_number, email,password=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not mobile_number:
            raise ValueError('Users must have an mobile_number')
        user = self.model(
            email=self.normalize_email(email),
            first_name = first_name,
            last_name = last_name,
            mobile_number =mobile_number,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, mobile_number,email, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            first_name=first_name,
            last_name=last_name,
            mobile_number=mobile_number,
            email = self.normalize_email(email),
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class Registration(AbstractBaseUser):
    first_name = models.CharField(max_length=100 , blank=False )
    last_name = models.CharField(max_length=100, blank=True)
    mobile_number = models.CharField(max_length=10, unique=True)
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    role_id = models.ForeignKey(Role, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'mobile_number'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email', 'user_type_id']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin




from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail

@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):

    # permission_classes = (IsAuthenticated,)

    email_plaintext_message = "{}?token={}".format(reverse('password_reset:reset-password-request'), reset_password_token.key)

    send_mail(
        # title:
        "Password Reset for {title}".format(title="Some website title"),
        # message:
        email_plaintext_message,
        # from:
        "amahafujul44@gmail.com",
        # to:
        [reset_password_token.user.email]
    )
