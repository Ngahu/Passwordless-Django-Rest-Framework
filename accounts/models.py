from django.db import models
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser
    )
from django.conf import settings

#for the token creation 
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token



#generate a token for evert user created
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)




class UserManager(BaseUserManager):
    """
    Description:The user model mamanger.\n
    """
    def create_user(
                    self,
                    phone_number,
                    email=None,
                    password=None,
                    is_active=True,
                    is_staff=False,
                    is_admin=False,
                    ):
        if not phone_number:
            raise ValueError("Users must have an phone number!")
        
        if not password:
            raise ValueError("Users must have a password!")

        user_obj  = self.model(
            phone_number = phone_number,
            email = self.normalize_email(email)
        )
        user_obj.set_password(password) 
        user_obj.staff = is_staff
        user_obj.admin=is_admin
        user_obj.active=is_active

        user_obj.save(using=self._db)
        return user_obj

    
    def create_staffuser(self,phone_number,email=None,password=None):
        """
        A method to create a staff user.
        """
        user = self.create_user(
            phone_number,
            email=email,
            password=password,
            is_staff=True
        )
        return user
    

    def create_superuser(self,phone_number,email=None,password=None):
        """
        A method to create the super user
        """
        user = self.create_user(
            phone_number,
            email=email,
            password=password,
            is_staff=True,
            is_admin=True,
        )
        return user

    











class User(AbstractBaseUser):
    phone_number = models.CharField(db_index=True,max_length=100,verbose_name='phone number',unique=True)
    email = models.EmailField(db_index=True,verbose_name='email address',max_length=255,unique=True,blank=True, null=True)
    # Each `User` needs a human-readable unique identifier that we can use to
    # represent the `User` in the UI. We want to index this column in the
    # database to improve lookup performance.
    first_name = models.CharField(max_length=100,blank=True, null=True)
    last_name = models.CharField(max_length=100,blank=True, null=True)
    active = models.BooleanField(default=True)  #can login or not
    # active = models.BooleanField(default=True)  #can login or not
    staff = models.BooleanField(default=False) # a superuser
    admin = models.BooleanField(default=False) # a admin user; non super-user

    timestamp = models.DateTimeField(auto_now_add=True)
    # notice the absence of a "Password field", that's built in.

    USERNAME_FIELD = 'phone_number'
    # REQUIRED_FIELDS = ['']

    objects = UserManager()


    def __str__(self):
        return str(self.phone_number)
    


    def get_full_name(self):
        # The user is identified by their phone_number
        return self.phone_number

    def get_short_name(self):
        # The user is identified by their phone_number
        return self.phone_number
    
    def has_perm(self,perm,obj=None):
        #Does the user have a specific permission?
        # Simplest possible answer: Yes, always
        return True

    
    def has_module_perms(self,app_label):
        #"Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True
    

    
    @property
    def is_staff(self):
        if self.is_admin:
            return True
        return self.staff
    

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_active(self):
        return self.active

    
    


