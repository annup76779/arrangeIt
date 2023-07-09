import random
import string

from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.contrib.auth.models import AbstractUser


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_superuser(self, email, password, **extra_fields):
        return self.create_user(email, password, **extra_fields)

    def create_user(self, email, password, **extra_fields):
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(self._db)

        return user


def generate_unique_key(n=6):
    characters = string.ascii_letters + string.digits
    key = ''.join(random.choice(characters) for _ in range(n))
    return key


class User(AbstractUser):
    class Role(models.TextChoices):
        ORG = 1, "Organization"
        MEMBER = 2, "Member"

    base_role = Role.ORG

    username = None
    email = models.CharField(max_length=255, unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    role = models.IntegerField(choices=Role.choices)
    member = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)

    objects = UserManager()

    def save(self, *args, **kwargs):
        if not self.pk:
            self.role = self.base_role
        return super().save(*args, **kwargs)

    class Meta:
        unique_together = ('email', "role")


class OrganizationManager(UserManager):
    def get_queryset(self, *args, **kwargs):
        result = super().get_queryset(*args, **kwargs)
        return result.filter(role=User.Role.ORG)


class OrganizationUser(User):
    base_role = User.Role.ORG

    objects = OrganizationManager()

    class Meta:
        proxy = True

    def __str__(self):
        return self.email


class OrgJoinCodes(models.Model):
    join_code = models.CharField(max_length=9, primary_key=True)
    user = models.OneToOneField(OrganizationUser, on_delete=models.CASCADE, related_name="join_code")


class MemberManager(UserManager):
    def create_user(self, email, password, **extra_fields):
        try:
            join_obj = OrgJoinCodes.objects.get(join_code=extra_fields.pop('join_code'))
            user = self.model(email=email, member=join_obj.user, **extra_fields)
            user.set_password(password)
            user.save(self._db)

            # manage Roles here.

            return user
        except OrgJoinCodes.DoesNotExist:
            raise Exception("No organization with provided join-code is available.")

    def get_queryset(self, *args, **kwargs):
        result = super().get_queryset(*args, **kwargs)
        return result.filter(role=User.Role.MEMBER)


class MemberUser(User):
    base_role = User.Role.ORG

    objects = MemberManager()

    class Meta:
        proxy = True

    def __str__(self):
        return "MEMBER: %s" % self.email


class Role(models.Model):
    organization = models.ForeignKey(OrganizationUser, on_delete=models.CASCADE, related_name="created_role")
    name = models.CharField(max_length=255)
    add_time_table = models.BooleanField(default=False)
    update_status = models.BooleanField(default=False)
    date_of_creating = models.DateTimeField(auto_now_add=True)
