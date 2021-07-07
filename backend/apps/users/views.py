import datetime

from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from backend.apps.users.models import User


class UserDetailsView(APIView):
    """
    API to get user details
    """
    def get(self, request, *args, **kwargs):
        user_id = kwargs['user_id']
        if not user_id:
            return Response({'status': "Mandatory data missing"}, status=404)

        user = User.objects.filter(id=user_id).first()
        user_response = {'id': user_id, 'first_name':user.first_name,'last_name':user.last_name,'username': user.username, 'short_desc': user.short_desc,
                         'email': user.email, 'is_active': user.is_active}
        return Response(user_response, status.HTTP_200_OK)

    def post(self, request,user_id):
        """
        API to update User details
        """
        user_id = user_id
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        email = request.data.get('email')
        short_desc = request.data.get('short_desc')

        if not all([first_name, last_name, email, user_id]):
            return Response({"status":"All the fields are mandatory"}, status=400)

        user = User.objects.filter(id=user_id).first()

        if not user:
            return HttpResponse("Incorrect User Id", status=400)

        with transaction.atomic():
            user.first_name = first_name.strip()
            user.last_name = last_name.strip()
            user.email = email
            user.short_desc = short_desc
            user.updated_at = datetime.datetime.now()
            user.save()

        return HttpResponse("Updated successfully", status=200)


