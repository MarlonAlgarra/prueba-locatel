from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, username, first_name, last_name, email ,password=None, **extra_fields):
        if not username:
            raise ValueError("El campo 'username' debe ser proporcionado.")
        user = self.model(username=username,first_name=first_name, last_name=last_name, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, first_name, last_name, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("El superusuario debe tener 'is_staff=True'.")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("El superusuario debe tener 'is_superuser=True'.")
        return self.create_user(username, password, first_name=first_name, last_name=last_name, email=email, **extra_fields)

class User(AbstractBaseUser):
    username = models.PositiveIntegerField(unique=True)
    first_name = models.CharField(max_length=100, default= '')
    last_name = models.CharField(max_length=100, default= '')
    email = models.EmailField(max_length=100, default='')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    objects = CustomUserManager()
    USERNAME_FIELD = 'username'

class Banks(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    code = models.CharField(max_length=5)
    def __str__(self):
        return self.name

class Accounts(models.Model):
    account_number = models.CharField(max_length=20)
    owner = models.CharField(max_length=100)
    owner_document = models.CharField(max_length=20, default='')
    holder = models.ForeignKey('User',on_delete=models.CASCADE)
    bank = models.ForeignKey('Banks', on_delete=models.CASCADE)
    balance = models.DecimalField(decimal_places=2, max_digits=9)
    def __str__(self):
        return self.account_number

class History(models.Model):
    transactionType = models.CharField(max_length=15)
    date_time = models.DateTimeField(auto_now_add=True)
    value = models.DecimalField(decimal_places=2, max_digits=9)
    account = models.ForeignKey(Accounts, on_delete=models.CASCADE) 
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    track_id = models.CharField(max_length=15, default='')

    def __str__(self):
        return f"{self.date_time} - {self.transactionType}"
    