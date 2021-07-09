from django.urls import path
from django.urls import path, include
from apps.users import views

urlpatterns = [
    path('details/<int:user_id>', views.UserDetailsView.as_view())
]