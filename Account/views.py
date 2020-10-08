# from django.contrib.auth import logout
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import api_view, permission_classes
# from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.hashers import check_password
from rest_framework.views import APIView
from Account.models import Registration
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout as signout
# from django.db import connection
from response_handle import exception_handler
from .serializers import RegisterSerializer, UserUpdateSerializer,ChangePasswordSerializer
# from drf_yasg.utils import swagger_auto_schema

from django.core.mail import BadHeaderError, send_mail
from rest_framework.permissions import IsAuthenticated
from rest_framework import permissions, decorators, status
from rest_framework_simplejwt.tokens import RefreshToken





@api_view(['GET'])
def ab(request):
    return "hello !!"

# -----------------------------------------------------

@api_view(['POST'])
def user_registration(request):

    if not request.data:
            return exception_handler.error_handling(errMsg="Invalid access.")
    registration = request.data
    if not registration:
        return exception_handler.error_handling(errMsg="User registration form should not empty.")


    mobile_number = Registration.objects.filter(mobile_number=request.data['mobile_number'])
    email = Registration.objects.filter(email=request.data['email'])

    if len(mobile_number)!=0:
        return exception_handler.error_handling(errMsg="Mobile number is already register.")
        # output = {"mobile_number": "mobile number is already register", "status": "failed"}
        # return Response(output, status=status.HTTP_400_BAD_REQUEST)

    if len(email)!=0:
        return exception_handler.error_handling(errMsg="Email id is already register.")

    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()

        result = {"registration":serializer.data}
        return exception_handler.error_handling(data=result, status_code=201)
        # output = {"result": serializer.data, "status": "success"}
        # return Response(output, status=status.HTTP_201_CREATED)
    else:

        array_error = serializer.errors
        return exception_handler.error_handling(array_error=array_error, errMsg="invalid access")
        # output = {"error": serializer.errors, "status": "failed"}
        # return Response(output, status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_400_BAD_REQUEST)


# -----=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

@api_view(['POST'])
# @permission_classes([IsAuthenticated])
# @permission_classes([permissions.AllowAny])
def userlogin(request):

    # print(request.user.id)
    if not request.data:
        return exception_handler.error_handling(errMsg="Invalid Access")
    mobile_number = request.data['mobile_number']
    password = request.data['password']

    if mobile_number == '':
        output = "Mobile number is empty."
        return exception_handler.error_handling(errMsg=output)
    elif password == '':
        output = "password is empty."
        return exception_handler.error_handling(errMsg=output)
    try:
        myuser = Registration.objects.get(mobile_number__exact=mobile_number)
    except Registration.DoesNotExist:
        output = "Registration id does not exist."
        return exception_handler.error_handling(errMsg=output)

    if not check_password(password, myuser.password):
        output = "Password is wrong!"
        return exception_handler.error_handling(errMsg=output)
    else:
        user = True
    print(myuser.password,"password......")

    if user is not None:

        login(request, myuser)
        refresh = RefreshToken.for_user(myuser)
        res = {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }
        user_details = {
                            'user.id':myuser.pk,
                            'first_name':myuser.first_name,
                            'last_name':myuser.last_name,
                            'email':myuser.email,
                            'is_admin':myuser.is_admin
                            }

        result = {'user_details':user_details, 'token':res}
        return exception_handler.error_handling(data=result, status_code=200)

    else:
        output = "User id is none."
        return exception_handler.error_handling(errMsg=output)

    return Response(status=status.HTTP_400_BAD_REQUEST)


# -----------------------------------------------------------------

@api_view(['PUT'])
def user_registration_update(request, user_id):
    if not request.data:
        output = {"error": serializer.errors, "status": "failed"}
        return Response(output, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = Registration.objects.get(id = user_id)
    except Registration.DoesNotExist:
        return exception_handler.error_handling(errMsg="This user is does not exist")

    print(user.mobile_number)
    print(user.email)
    print(user.id)


    print(request.data['first_name'])
    print(request.data['last_name'])


    serializer = RegisterSerializer(user, data=request.data)
    if serializer.is_valid():
        user.first_name = request.data['first_name']
        user.last_name = request.data['last_name']
        user.mobile_number = request.data['mobile_number']
        user.save()
        result = {"User_Registration":serializer.data}
        return exception_handler.error_handling( data=result, status_code=201)
    else:
        array_error = serializer.errors
        return exception_handler.error_handling(array_error=array_error, errMsg="Invalid access!!!")


# --------------------------------------------------------

@api_view(['PUT'])
def ChangePasswordView(request, user_id):
    permission_classes = (IsAuthenticated,)

    if not request.data:
        return exception_handler.error_handling(errMsg="Invalid Access")
    old_password = request.data['old_password']
    new_password = request.data['new_password']

    if old_password == '':
        return exception_handler.error_handling(errMsg="Old password is empty.")

    if new_password == '':
        return exception_handler.error_handling(errMsg="New password is empty.")

    try:
        user = Registration.objects.get(id= user_id)
    except Registration.DoesNotExist:
        return exception_handler.error_handling(errMsg="This id does not exist")


    if not check_password(old_password, user.password):
        output = "Password is wrong!"
        return exception_handler.error_handling(errMsg=output)

    user.set_password(new_password)
    user.save()
    return Response(status=status.HTTP_200_OK)


# ---------------------------------------------------------------------
# Email sending =====================
@api_view(['POST'])
def send_email(request):
    # permission_classes = (IsAuthenticated,)
    subject = request.POST.get("hey this is subject")
    message = request.POST.get("Hey this is message")
    # from_email = request.POST.get('hackingameworld@gmail.com')
    # if subject and message:
    #     try:
    send_mail("hey this is Alam",
                    "Alam is saing that u r hacked!!!  hihiihihihih",
                    'amahafujul44@gmail.com',
                    ['ansarisiraj381@gmail.com'],
                    fail_silently=False)
        # except BadHeaderError:
        #     return HttpResponse('Invalid header found.')
    return Response('done')
    # else:
    #     # In reality we'd use a form class
    #     # to get proper validation errors.
    #     return HttpResponse('Make sure all fields are entered and valid.')

# ----------------------------------------


