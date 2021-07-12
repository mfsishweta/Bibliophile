# Create your views here.
from rest_framework import status, renderers
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.users.models import User
from apps.users.serializer import UserUpdateSerializer


class UserDetailsView(APIView):
    """
    API to get user details
    """
    # permission_classes = (IsAuthenticated, )
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
