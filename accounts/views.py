import logging
from django.shortcuts import render

from django.contrib.auth import get_user_model
User = get_user_model()

logger = logging.getLogger(__name__)

from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from rest_framework import status

from django.conf import settings

from rest_framework.authtoken.models import Token
from certify.models import CallbackToken

from django.utils import timezone

from passwordless_drf.settings import DEFAULTS

import africastalking

from .serializers import UserCreateSerializer

PASSWORDLESS_AFRICAS_TALKING_USERNAME = getattr(settings, 'PASSWORDLESS_AFRICAS_TALKING_USERNAME', None)

PASSWORDLESS_AFRICAS_TALKING_API_KEY = getattr(settings, 'PASSWORDLESS_AFRICAS_TALKING_API_KEY', None)

PASSWORDLESS_AFRICAS_TALKING_SENDER_ID = getattr(settings, 'PASSWORDLESS_AFRICAS_TALKING_SENDER_ID', None)


PASSWORDLESS_TOKEN_EXPIRE_TIME = getattr(settings, 'PASSWORDLESS_TOKEN_EXPIRE_TIME', 900) #900 seconds


africastalking.initialize(PASSWORDLESS_AFRICAS_TALKING_USERNAME,PASSWORDLESS_AFRICAS_TALKING_API_KEY)

# Initialize a service e.g. SMS
sms = africastalking.SMS





def create_callback_token_and_send_to_user(user):
    """
    Description::This is responsible to create a call back token for 
                the user and then send it to their point of contact
                either phone or email or both.\n
    
    Takes in a user as an arguement
    """
    pass






def validate_token_age(callback_token):
    """
    Returns True if a given token is within the age expiration limit.
    """
    try:
        token = CallbackToken.objects.get(key=callback_token, is_active=True)
        seconds = (timezone.now() - token.created_at).total_seconds()
        token_expiry_time = PASSWORDLESS_TOKEN_EXPIRE_TIME

        print("token_expiry_time",token_expiry_time)

        if seconds <= token_expiry_time:
            return True
        else:
            # Invalidate our token.
            token.is_active = False
            token.forced_expired = True
            token.save()
            return False

    except CallbackToken.DoesNotExist:
        # No valid token.
        return False




class RootAPIView(APIView):
    """
    returns a list of all the urls for this app
    """
    # permission_classes = (IsAuthenticated)
    def get(self,request,format=None):
        return Response({
            "authenticate":reverse("accounts_auth:user_authenticate", request=request, format=format), 
            "confirm":reverse("accounts_auth:user_confirm_api_view", request=request, format=format), 
        })






class UserAuthenticateAPIView(APIView):
    '''
    Description:\n Authenticate a user by their phone number.If user
                exists they receive a validation code to either their phone number
                or their email or both.\n
                If the user is new an account is created for them and a code sent to 
                their  phone number and email.\n
    Type of request: POST\n,
    Request data type: JSON\n
    POST request body:\n {
    "phone_number": "+254725743069",
    }\n
    Response success Status: HTTP_200_OK\n
    Response data type: JSON\n
    Sample success Response: \n
    {
    "status": "success",
    "message": "Verification Code sent to +254725743069",
    "token": null
    }
    \n
    Response failure: \n{
    error: "Oops!Its not you. Its us. Give it another try please.": \t HTTP_400_BAD_REQUEST
    }\n
    '''
    def post(self,request,*args,**kwargs):
        phone_number = request.data["phone_number"]

        #First make sure that the user is registered
        try:
            the_user = User.objects.get(
                phone_number=phone_number
            )

            #if user exists generate a key for them
            generated_key = CallbackToken.objects.create(user=the_user)
            print("generated_key",generated_key)

            #then send the code to the user phone number
            text_message = "{} is your eLimu verification code.".format(generated_key.key)
            
            sender = PASSWORDLESS_AFRICAS_TALKING_SENDER_ID

            phone_numbers_list = []


            phone_numbers_list.append(str(the_user.phone_number))


            

            res = sms.send(message=text_message,recipients=phone_numbers_list,sender_id=sender)

            print(res)

            verify_sms_response = {
                "status":"success",
                "message":"Verification Code sent to {}".format(phone_number),
                "token":None
            }
            
            return Response(verify_sms_response,status=status.HTTP_202_ACCEPTED)

        
        except User.DoesNotExist:
            #create a new user here and then create a key then send it to them

            data = {
                "phone_number":phone_number
            } 

            usercreate_serializer = UserCreateSerializer(data=data)

            if usercreate_serializer.is_valid():
                user = usercreate_serializer.save()
                user.set_unusable_password()
                user.save()

                #Generate the key here
                new_user_key = CallbackToken.objects.create(user=user)

                #Send the code to the user
                text_message = "{} is your eLimu verification code.".format(new_user_key.key)

                sender = PASSWORDLESS_AFRICAS_TALKING_SENDER_ID

                phone_numbers_list = []

                phone_numbers_list.append(str(user.phone_number))

                res = sms.send(message=text_message,recipients=phone_numbers_list,sender_id=sender)
                print(res)

                verify_sms_response = {
                "status":"success",
                "message":"Verification Code sent to {}".format(phone_number),
                "token":None
                }


                return Response(verify_sms_response,status=status.HTTP_202_ACCEPTED)

            return Response(usercreate_serializer.errors,status=status.HTTP_400_BAD_REQUEST)





class UserConfirmAPIView(APIView):
    '''
    Description:\n Confirm  a user by their phone number\n
    Type of request: POST\n,
    Request data type: JSON\n
    POST request body:\n {
	"verification_code":"1395",
	"phone_number":"+254736425236"
    }\n
    Response success Status: HTTP_200_OK\n
    Response data type: JSON\n
    Sample success Response: \n
    {
    "status": "success",
    "token": "d4b0712d6313502701d3ddcea818cc2988099073",
    "message": "Success user Authentication"
    }
    \n
    Response failure: \n{
    error: "Oops!Its not you. Its us. Give it another try please.": \t HTTP_400_BAD_REQUEST
    }\n
    '''
    def post(self,request,*args,**kwargs):
        verification_code = request.data['verification_code']
        phone_number = request.data["phone_number"]

        #first make sure that the user is registered
        try:
            user = User.objects.get(
                phone_number=phone_number
            )

            #if the user exists make sure the verification_code is valid too and also active

            try:
                the_code = CallbackToken.objects.get(key=verification_code,is_active=True)

                #make sure the one using the code is the owner
                if the_code.user != user:
                    logger.warning("drfpasswordless: User passed a code that does not belong to them.")
                    verify_sms_response = {
                        "status":"error",
                        "token":None,
                        "message":"Please try again ,Wrong Velification."
                    }
                    
                    return Response(verify_sms_response,status=status.HTTP_400_BAD_REQUEST)
                
                #make sure the code is not expired
                is_valid = validate_token_age(the_code)

                if is_valid:
                    #mark the code as used 
                    the_code.is_active = False
                    the_code.is_used = True
                    the_code.date_used = timezone.now()
                    the_code.save()

                    #get the user auth token 
                    try:
                        token = Token.objects.get(user_id=user.id)

                        verify_sms_response = {
                            "status":"success",
                            "token":token.key,
                            "message":"Success user Authentication",
                            # "phone_number":user.phone_number,
                            # "email":user.email,
                            # "first_name":user.first_name,
                            # "last_name":user.last_name,
                        }
                        return Response(verify_sms_response,status=status.HTTP_202_ACCEPTED)

                    except Token.DoesNotExist:
                        logger.debug("passwordlessdrf: Challenged to obtain non-existing user token.")
                        error = {
                            "error":"Sorry This  user is not active please contact us!"
                        }
                        return Response(error,status=status.HTTP_400_BAD_REQUEST)
                
                verify_sms_response = {
                    "status":"error",
                    "token":None,
                    "message":"Sorry,Your code is expired."
                }
                return Response(verify_sms_response,status=status.HTTP_400_BAD_REQUEST)
            

            except CallbackToken.DoesNotExist:
                logger.debug("drfpasswordless: Challenged with a callback token that doesn't exist.")

                verify_sms_response = {
                    "status":"error",
                    "token":None,
                    "message":"Your code does not exist"
                }
                return Response(verify_sms_response,status=status.HTTP_400_BAD_REQUEST)
        
        except User.DoesNotExist:
            logger.debug("drfpasswordless: Authenticated user somehow doesn't exist.")
            verify_sms_response = {
                "status":"error",
                "token":None,
                "message":"You are not registered"
            }
            return Response(verify_sms_response,status=status.HTTP_400_BAD_REQUEST)






