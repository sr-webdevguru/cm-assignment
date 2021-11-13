import uuid

from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver
from rest_framework.authtoken.models import Token

SOLO = 0
NETWORK = 1
UserConnected = (
    (SOLO, 'solo'),
    (NETWORK, 'network')
)


class CustomUserManager(BaseUserManager):
    """
    Manages the custom user model
    create_user : for creating general user
    create_superuser : for creating admin user
    """

    def create_user(self, email, name):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            name=name,
        )

        # sets random 10 character length password for user
        password = self.make_random_password(length=10,
                                             allowed_chars='abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789')
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password):
        user = self.model(
            email=self.normalize_email(email),
            name=name,
        )

        user.set_password(password)
        user.is_admin = True
        user.save(using=self._db)
        return user


class Users(AbstractBaseUser):
    user_pk = models.AutoField(primary_key=True)
    user_id = models.UUIDField(verbose_name="user unique id", default=uuid.uuid4, editable=False)
    email = models.EmailField(verbose_name="user email", max_length=254, unique=True)
    phone = models.CharField(max_length=20, verbose_name="user phone number", blank=True, null=True)
    name = models.CharField(verbose_name="user full name", max_length=254)
    locale = models.CharField(verbose_name="user locale", max_length=10, default="en_US")
    user_connected = models.IntegerField(choices=UserConnected, verbose_name="user connected state", default=SOLO)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    user_controlled_substances = models.BooleanField(verbose_name="user controlled substances", default=False)
    user_asset_management = models.BooleanField(verbose_name="user asset management", default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    objects = CustomUserManager()

    def __unicode__(self):
        return self.email

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.name

    # For custom model to work with admin
    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    class Meta:
        ordering = ["name"]

    # Admin required fields
    @property
    def is_staff(self):
        return self.is_admin


class UserRoles(models.Model):
    role_id = models.AutoField(primary_key=True)
    key = models.CharField(max_length=140, verbose_name="user role key")
    order = models.IntegerField(verbose_name="user role order")

    def __unicode__(self):
        return str(self.role_id)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created and (not kwargs.get('raw', False)):
        Token.objects.create(user=instance)
