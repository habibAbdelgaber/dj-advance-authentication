from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser, UserManager

class AccountManager(UserManager):
    def create_user(self, first_name, last_name, username, email, password=None):
        if not username:
            raise ValueError('this username field is required!')
        if not email:
            raise ValueError('email field is required!')

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            username=username
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name,username,  email, password):
        user = self.create_user(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            username=username,
            password=password
        )

        user.is_active = True
        user.is_superadmin = True
        user.is_staff = True
        user.is_admin = True
        user.save(using=self._db)
        return user

class Account(AbstractBaseUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    email = models.CharField(max_length=50, unique=True)
    phone_number = models.CharField(max_length=100)

    password = models.CharField(max_length=100)

    objects = AccountManager()

    def __str__(self):
        return self.email



    # REQUIRED FIELD

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'username']

    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)


    def has_perm(self, perm, obj=None):
        return self.is_superadmin

    def has_module_perms(self, perm, app_label=None):
        return True

