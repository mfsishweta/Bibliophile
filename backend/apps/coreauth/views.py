from django.http import JsonResponse
from rest_framework import renderers, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from .otp_service.otp_manager import OTPAuthenticationRecordGenerator, EmailSender
from .serializers import MyTokenObtainPairSerializer, RegisterSerializer


class BearerAuthentication(TokenAuthentication):
    keyword = 'Bearer'


class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer


class RegisterView(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class VerifyOTPView(APIView):
    renderer_classes = [renderers.JSONRenderer]

    authentication_classes = (BearerAuthentication,)
    permission_classes = (IsAuthenticated,)

    # TODO:after verifying the otp make the user active
    def post(self, request):
        otp = request.GET.get('otp')
        user = request.user
        is_valid = OTPAuthenticationRecordGenerator().validate_otp(user.id, otp)
        if is_valid:
            user.email_verified = True
            user.save(update_fields=['email_verified'])
            return JsonResponse({'result': "Email successfully verified"}, status=status.HTTP_200_OK)

        else:
            return JsonResponse({'result': "Wrong OTP, please try again"}, status=status.HTTP_200_OK)


class ResendOTPView(APIView):
    renderer_classes = [renderers.JSONRenderer]

    authentication_classes = (BearerAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        user = request.user
        EmailSender().create_and_send_email(user.id)
        return JsonResponse({'result': "Email successfully verified"}, status=status.HTTP_200_OK)
