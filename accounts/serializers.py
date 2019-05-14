from rest_framework import serializers
from django.contrib.auth import get_user_model
User = get_user_model()




class UserCreateSerializer(serializers.ModelSerializer):
    """
    Description:The serializer to validate the user details during registration\n
    """

    class Meta:
        model = User
        fields = (
            'phone_number',
        )
        read_only_fields = ('is_staff', 'is_admin', 'is_active',)

        def create(self,validated_data):
            user = User(
                phone_number=validated_data['phone_number']
            )
            user.set_unusable_password()
            user.save()
            
            return user






class ReadUserSerializer(serializers.ModelSerializer):
    '''
    Description: Returns a read only user details
    '''
    class Meta:
        model = User
        fields = [
            'phone_number',
            'email',
            'first_name',
            'last_name'
        ]
