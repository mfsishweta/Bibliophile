from django.http import JsonResponse
from rest_framework import renderers, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from apps.users.models import User
from .otp_service.otp_manager import OTPAuthenticationRecordGenerator, EmailSender
from .serializers import MyTokenObtainPairSerializer, RegisterSerializer


class BearerAuthentication(TokenAuthentication):
    keyword = 'Bearer'


class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer


class LoginView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        """
        API to login user
        """
        username = request.data.get('username')
        password = request.data.get('password')
        if username is None or password is None:
            return Response({'error': 'Please provide both username and password'},
                            status.HTTP_400_BAD_REQUEST)
        user_obj = User.objects.filter(
            username=username, is_active=True).first()
        if not user_obj:
            return Response('No record for this username', status.HTTP_404_NOT_FOUND)
        if user_obj.check_password(password):
            token = Token.objects.filter(user=user_obj).first()
            data = {'user_id': user_obj.id, 'username': user_obj.username, 'token': token.key}
            return Response(data, status.HTTP_200_OK)
        return Response('wrong username and password', status.HTTP_400_BAD_REQUEST)


class RegisterView(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class SignupView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer_class = RegisterSerializer


class VerifyOTPView(APIView):
    renderer_classes = [renderers.JSONRenderer]
    authentication_classes = (BearerAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        otp = request.data.get('otp')
        user = request.user
        is_valid = OTPAuthenticationRecordGenerator().validate_otp(user, otp)
        if is_valid:
            user.email_verified = True
            user.save(update_fields=['email_verified'])
            return JsonResponse({'result': "Email successfully verified"}, status=status.HTTP_200_OK)

        else:
            return JsonResponse({'result': "Wrong OTP, please try again"}, status=status.HTTP_200_OK)


class ResendOTPView(APIView):
    renderer_classes = [renderers.JSONRenderer]

    # authentication_classes = (BearerAuthentication,)
    # permission_classes = (IsAuthenticated,)

    def post(self, request):
        user = request.user
        EmailSender().create_and_send_email(user.id)
        return JsonResponse({'result': "Email successfully verified"}, status=status.HTTP_200_OK)
