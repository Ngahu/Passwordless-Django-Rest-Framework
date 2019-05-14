'''Utility Methods for the project.'''
import random




from django.utils import timezone


from django.conf import settings






ALLOWED_INT = '0123456789'



def random_string_generator(size=10,chars=ALLOWED_INT):
    '''
    Description:Generate random values based on the size and chars passed.\n
    '''
    return ''.join(random.choice(chars) for _ in range(size))






def custom_key_generator(instance,size=4):
    '''
    Description:Generate a unique key for every instance passed.\n
    '''
    new_key = random_string_generator(size=size)

    # get the class from the instance
    Klass = instance.__class__

    # qs_exists = Klass.objects.filter(key=new_key).exclude(is_active=True).exists()
    qs_exists = Klass.objects.filter(key=new_key).exists()
    if qs_exists:
        return custom_key_generator(size=size)
    
    return new_key









