from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from Account import views

urlpatterns = [

    path('ab', views.ab),
    # path('user_authenticate', views.user_authenticate),
    path('userlogin',views.userlogin),
    path('user_registration',views.user_registration),
    # path('user_profile',views.user_profile),
    path('ChangePasswordView/<int:user_id>', csrf_exempt(views.ChangePasswordView)),
    path('user_registration_update/<int:user_id>',views.user_registration_update),
    path('send_email',views.send_email),

]
