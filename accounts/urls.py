from django.conf.urls import url
from .views import(
    UserAuthenticateAPIView,
    RootAPIView,
    UserConfirmAPIView
)

urlpatterns = [
    
    url('api/v1/$', RootAPIView.as_view(), name='root_api_v1'),
    url('authenticate/$', UserAuthenticateAPIView.as_view(), name='user_authenticate'),
    url('confirm/$', UserConfirmAPIView.as_view(), name='user_confirm_api_view'),
    
]



