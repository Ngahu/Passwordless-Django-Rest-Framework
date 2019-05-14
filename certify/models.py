import uuid
from django.db import models
from django.db.models.signals import pre_save,post_save

from django.conf import settings

User = settings.AUTH_USER_MODEL
from django.utils.translation import gettext_lazy as _

from passwordless_drf.core.utils import custom_key_generator

from django.dispatch import receiver



class CallbackTokenManger(models.Manager):
    def active(self):
        return self.get_queryset().filter(is_active=True)

    def inactive(self):
        return self.get_queryset().filter(is_active=False)












class CallbackToken (models.Model):
    '''
    Description:This is going to be the handle all the tokens sent to the users.\n
    '''
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    is_invalidated = models.BooleanField(default=False)
    '''When a user creates a key all their previous active keys are
           invalidated.This way only one key is active.
           We want to know whether the key was invalidated and when used
           it is captured in the is_used field.
    '''
        
    key     = models.CharField(max_length=10,db_index=True,unique=True, blank=True) #length is 4 digits

    is_used = models.BooleanField(default=False)

    date_used = models.DateTimeField(blank=True, null=True)

    forced_expired  = models.BooleanField(default=False) #whether the code was forced to expire
    expires         = models.IntegerField(default=7) # 7 Days #How long a code should stay before expiring 
    update          = models.DateTimeField(auto_now=True)


    objects = CallbackTokenManger()



    

    class Meta:
        ordering = ['-created_at']
        

    def __str__(self):
        return str(self.key)

    def get_absolute_url(self):
        pass





def key_pre_save_receiver(sender,instance,*args,**kwargs):
    """
    Description:Create a key for every saved instance.\n
    """
    if not instance.key:
        instance.key = custom_key_generator(instance)


pre_save.connect(key_pre_save_receiver,sender=CallbackToken)







# def pre_save_invalidate_previous_keys_receiver(sender,instance,*args,**kwargs):
#     '''
#     Description:Invalidates all previously issued active keys.
#     '''
#     active_keys = None
#     if isinstance(instance, CallbackToken):
#         active_keys = CallbackToken.objects.active().filter(user=instance.user).exclude(id=instance.id)
    
#     # Invalidate keys
#     if active_keys:
#         print("active_keys",active_keys)
#         for token in active_keys:
#             token.is_active      =  False
#             token.is_invalidated =  True
#             print("token",token)
#             print("token",token.is_active)
#             print("token",token.is_invalidated)
#             token.save()


# pre_save.connect(pre_save_invalidate_previous_keys_receiver,sender=CallbackToken)



@receiver(post_save, sender=CallbackToken)
def pre_save_invalidate_previous_keys_receiver(sender,instance,created,*args,**kwargs):
    '''
    Description:Invalidates all previously issued active keys.
    '''
    if created:
        active_keys = None
        if isinstance(instance, CallbackToken):
            active_keys = CallbackToken.objects.active().filter(user=instance.user).exclude(id=instance.id)
        
        # Invalidate keys
        if active_keys:
            print("active_keys",active_keys)
            for token in active_keys:
                token.is_active      =  False
                token.is_invalidated =  True
                
                token.save()
                
