import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


class UserRole(models.IntegerChoices):
    ADMIN = 1
    ACCOUNTANT = 2
    MANAGER = 3
    EMPLOYEE = 4


class User(AbstractUser):
    public_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    role = models.PositiveSmallIntegerField(
        choices=UserRole.choices, default=UserRole.EMPLOYEE
    )

    def __str__(self):
        return f'{self.email}'

    @property
    def role_display(self):
        return self.get_role_display()

    @property
    def is_admin(self):
        return self.role == UserRole.ADMIN

    @property
    def is_accountant(self):
        return self.role == UserRole.ACCOUNTANT

    @property
    def is_manager(self):
        return self.role == UserRole.MANAGER

    @property
    def is_employee(self):
        return self.role == UserRole.EMPLOYEE
