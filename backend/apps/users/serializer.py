from rest_framework.serializers import ModelSerializer

from apps.users.models import User


class UserDetailsSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'short_desc', 'username', 'email_verified')


class UserUpdateSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'short_desc')
        extra_kwargs = {
            'first_name': {'required': False},
            'last_name': {'required': False},
            'short_desc': {'required': False},
            'username': {'required': False},
        }

    def update(self, instance: User, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.short_desc = validated_data.get('short_desc', instance.short_desc)
        instance.save()
        return instance
