# Create your views here.
import traceback

from django.db import transaction
from django.http import JsonResponse
from rest_framework import status, renderers
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import APIException
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.users.models import User, FriendRequest
from apps.users.serializer import UserUpdateSerializer


class BearerAuthentication(TokenAuthentication):
    keyword = 'Bearer'


class UserDetailsView(APIView):
    """
    API to get user details
    """
    permission_classes = (IsAuthenticated,)
    renderer_classes = [renderers.JSONRenderer]

    def get(self, request, user_id):
        """
        API to get User details
        """
        try:
            user = User.objects.get(id=user_id)
            user_response = {'id': user_id, 'first_name': user.first_name, 'last_name': user.last_name,
                             'username': user.username, 'short_desc': user.short_desc,
                             'email': user.email, 'is_active': user.is_active}
            return Response(user_response, status.HTTP_200_OK)
        except Exception as e:
            return APIException(str(e))

    def post(self, request, user_id):
        """
        API to update User details
        """
        user = User.objects.get(id=user_id)
        serializer = UserUpdateSerializer(user, data=request.data)
        if not serializer.is_valid():
            raise APIException(serializer.errors)
        serializer.save()
        return Response({'result': "Updated Successfully!"}, status=status.HTTP_200_OK)


# @login_required
class SendFriendRequestView(APIView):
    """
    API to send friend request
    """
    renderer_classes = [renderers.JSONRenderer]

    authentication_classes = (BearerAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        from_user = request.user
        friend_user = request.GET.get('friend_user_id')
        to_user = User.objects.filter(id=friend_user).first()
        try:
            friend_request = FriendRequest.objects. \
                filter(from_user=from_user, to_user=to_user).first()
            if not friend_request:
                fd = FriendRequest()
                fd.from_user = from_user
                fd.to_user = to_user
                fd.save()
                return JsonResponse({'result': "Friend Request Sent successfully!"}, status=status.HTTP_200_OK)
            else:
                return JsonResponse({'result': "Friend Request was already sent!"}, status=status.HTTP_200_OK)
        except Exception as e:
            return APIException(str(e))


class AcceptFriendRequestView(APIView):
    renderer_classes = [renderers.JSONRenderer]

    authentication_classes = (BearerAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, **kwargs):
        friend_request_id = request.GET.get('request_id')
        friend_request = FriendRequest.objects.filter(id=friend_request_id).first()
        try:
            if friend_request and friend_request.to_user == request.user:
                # with transaction.atomic:
                friend_request.to_user.friend.add(friend_request.from_user)
                friend_request.from_user.friend.add(friend_request.to_user)
                friend_request.to_user.save()
                friend_request.from_user.save()

                # friend_request.to_user.save(update_fields=['friend'])
                # friend_request.from_user.save(update_fields=['friend'])
                friend_request.delete()
                return JsonResponse({'result': "Friend Request Accepted!"}, status=status.HTTP_200_OK)
            else:
                return JsonResponse({'result': "Invalid friend request!"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            traceback.print_exc()
            return Response(str(e))
            # APIException(str(e))

