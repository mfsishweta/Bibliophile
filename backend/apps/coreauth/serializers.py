from django.contrib.auth.password_validation import validate_password
from django.db import transaction
from rest_framework.exceptions import ValidationError
from rest_framework.fields import EmailField, CharField
from rest_framework.serializers import ModelSerializer
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from apps.coreauth.otp_service.otp_manager import EmailSender
from apps.lists.models import UserList
from apps.users.models import User


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)

        # Add custom claims
        token['username'] = user.username
        return token


class RegisterSerializer(ModelSerializer):
    email = EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    password = CharField(write_only=True, required=True, validators=[validate_password])
    password2 = CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name', 'short_desc')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
            'short_desc': {'required': False},
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        with transaction.atomic():
            user = User.objects.create(
                **validated_data
            )

            user.set_password(validated_data['password'])

            user.save()
            # user = User.objects.get(email)
            UserList.objects.bulk_create([
                UserList(user=user, list='r'),
                 UserList(user=user, list='w'),
                 UserList(user=user, list='s')
            ])
            print('@@@@@@@@@@@@@@@@@@@@',user.username)
            EmailSender().create_and_send_email(user.id)

        return user
