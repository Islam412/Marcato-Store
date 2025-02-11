from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save  # create profile before creat user
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

from utils.generate_code import generate_code

# Create your models here.

class User(AbstractUser):
    first_name = models.CharField(_('Frist Name'),max_length=255, null=True, blank=True)
    last_name = models.CharField(_('Last Name'),max_length=255, null=True, blank=True)
    username = models.CharField(_('Username'),max_length=255, unique=True, null=True, blank=True)
    email = models.EmailField(_('Email'),unique=True)

    # Change defult django in adminbanal
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return str(self.username)
    



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cover_images = models.ImageField(_('Cover Image'),upload_to='Images_Profile', null=True, blank=True, default='user.png')
    address = models.OneToOneField('Address', null=True, blank=True, on_delete=models.SET_NULL)
    phone = models.OneToOneField('Phone', null=True, blank=True, on_delete=models.SET_NULL)
    code = models.CharField(max_length=10 ,default=generate_code)
    verified = models.BooleanField(_('Verified'),default=False)

    @property
    def first_name(self):
        return self.user.first_name
    
    @property
    def last_name(self):
        return self.user.last_name

    @property
    def username(self):
        return self.user.username
    
    @property
    def email(self):
        return self.user.email
    

    def __str__(self):
        return self.user.username if self.user and self.user.username else 'Unnamed Profile'
    
@receiver(post_save, sender=User)
# create user profile automatic
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

post_save.connect(create_user_profile ,sender=User)
post_save.connect(save_user_profile ,sender=User)



ADDRESS_TYPE = [
    ('Home', 'Home'),
    ('Work', 'Work'),
    ('Bussinees','Bussinees'),
    ('Office','Office'),
    ('Academy','Academy'),
    ('Other','Other'),
]

class Address(models.Model):
    user = models.ForeignKey(User,related_name='user_address',on_delete=models.CASCADE)
    type = models.CharField(max_length=20,choices=ADDRESS_TYPE)
    address = models.TextField(max_length=300)
    notes = models.TextField(null=True,blank=True)

    def __str__(self):
        return f"{self.type} - {self.address}"


Phone_TYPE = [
    ('Primary','Primary'),
    ('Secondary','Secondary'),
]


class Phone(models.Model):
    user = models.ForeignKey(User, related_name='user_phone', on_delete=models.CASCADE)
    type = models.CharField(max_length=20, choices=Phone_TYPE)
    phone = models.CharField(max_length=30)

    def clean(self):
        if not self.phone.isdigit():
            raise ValidationError("Phone number must be numeric.")

    def __str__(self):
        return f"{self.type} - {self.phone}"


