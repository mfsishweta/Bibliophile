from django.urls import path
from django.urls import path, include
from apps.users import views

urlpatterns = [
    path('details/<int:user_id>', views.UserDetailsView.as_view()),
    path('send-friend-request', views.SendFriendRequestView.as_view()),
    path('accept-friend-request', views.AcceptFriendRequestView.as_view()),
]