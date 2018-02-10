from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import RegexValidator

# Create your models here.


class BaseModel (models.Model):
    """
    Base Model is an abstract class that is extended by all
    other models. This includes creation time, last update time and visibility.
    Modifications to this class will alter all models!
    """

    creation_date = models.DateTimeField(auto_now_add=True)
    last_updated_date = models.DateTimeField(auto_now=True)
    visible = models.IntegerField(default=0)

    class Meta:
        abstract = True


class UserManager(BaseUserManager):

    def create_user(self, email, phone_number, password=None):
        if not email:
            raise ValueError('Users must have an email')
        if not phone_number:
            raise ValueError('Users must have a phone number')

        user = self.model(
            email=self.normalize_email(email),
            phone_number=phone_number,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, phone_number, password):
        user = self.create_user(
            email=self.normalize_email(email),
            phone_number=phone_number,
            password=password,
        )

        user.admin = True

        user.save(using=self._db)
        return user


class User(AbstractBaseUser, BaseModel):
    phone_regex = RegexValidator(regex=r'^\+\d{8,15}$',
                                 message="Phone number must be entered in the format: "
                                         "'+999999999'. Up to 15 digits allowed.")
    uid = models.AutoField(primary_key=True)
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=False, unique=True)
    email = models.EmailField(blank=False, unique=True)
    password = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['email', 'password']

    def get_full_name(self):
        return self.first_name + " " + self.last_name

    def get_short_name(self):
        return self.first_name[0] + ". " + self.last_name

    def get_username(self):
        return self.get_short_name();

    objects = UserManager()


class Conversation(BaseModel):
    cid = models.AutoField(primary_key=True)


class Message(BaseModel):
    mid = models.AutoField(primary_key=True)
    cid = models.ForeignKey(Conversation)
    message = models.TextField()


class Participants(BaseModel):
    cid = models.ForeignKey(Conversation)
    uid = models.ForeignKey(User)
