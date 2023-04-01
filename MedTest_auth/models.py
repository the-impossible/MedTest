from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.shortcuts import reverse
import uuid

# My app imports

# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, username, name, password=None):

        #creates a user with the parameters
        if username is None:
            raise ValueError('Username is required!')

        if name is None:
            raise ValueError('Full name is required!')

        if password is None:
            raise ValueError('Password is required!')

        user = self.model(
            username = username.upper().strip(),
            name = name.title().strip(),
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, username, name, password=None):
        # create a superuser with the above parameters

        user = self.create_user(
            username=username,
            name=name,
            password=password,
        )

        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save(using=self._db)

        return user

class User(AbstractBaseUser, PermissionsMixin):
    user_id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    username = models.CharField(max_length=20, db_index=True, unique=True, blank=True, null=True)
    name = models.CharField(max_length=60, db_index=True, blank=True)

    pic = models.ImageField(null=True, blank=True, upload_to='uploads/', default='img/user.png')

    date_joined = models.DateTimeField(verbose_name='date_joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last_login', auto_now=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'

    REQUIRED_FIELDS = ['name',]

    objects = UserManager()

    def __str__(self):
        return f'{self.username}'

    def has_perm(self, perm, obj=None):
        return self.is_staff

    def has_module_perms(self, app_label):
        return True

    class Meta:
        db_table = 'Users'
        verbose_name_plural = 'Users'

class Session(models.Model):
    session_title = models.CharField(max_length=9, unique=True)
    session_description = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.session_title

    class Meta:
        db_table = 'Session'
        verbose_name_plural = 'Sessions'

class Department(models.Model):
    dept_id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    dept_title = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.dept_title

    class Meta:
        db_table = 'Department'
        verbose_name_plural = 'Departments'

class College(models.Model):
    college_id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    college_title = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.college_title

    class Meta:
        db_table = 'College'
        verbose_name_plural = 'Colleges'


class Programme(models.Model):
    programme_title = models.CharField(max_length=30, unique=True)
    programme_description = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.programme_title

    class Meta:
        db_table = 'Programme'
        verbose_name_plural = 'Programmes'

class StudentProfile(models.Model):
    stud_id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    user_id = models.OneToOneField(User,blank=True, null=True, on_delete=models.CASCADE)
    programme = models.ForeignKey(Programme, on_delete=models.CASCADE)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    college = models.ForeignKey(College, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user_id}'

    class Meta:
        db_table = 'Student Profile'
        verbose_name_plural = 'Student Profile'
