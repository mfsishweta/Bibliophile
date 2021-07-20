from django.urls import path

from apps.books import views

urlpatterns = [

    path('details/<str:volume_id>', views.BookDetailsView.as_view()),
    path('search/', views.SearchBookItems.as_view()),
    path('get-ratings/', views.BookRatings.as_view()),
    path('save-book', views.SaveBookInListView.as_view()),

]
