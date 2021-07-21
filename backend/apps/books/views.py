import traceback

from django.db import transaction
from django.http import JsonResponse
from rest_framework import status, renderers
from rest_framework.exceptions import APIException
from rest_framework.generics import ListAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.books.google_book_data_storage import BooksDataExtractor, BODOAdapter
from apps.books.models import Book
from apps.books.serializers import BookRatingsSerializer, SearchBookQuerySerializer
from apps.coreauth.views import BearerAuthentication
from apps.feedbacks.models import UserBookRatingReviews
from apps.lists.models import UserList


class Paginator(LimitOffsetPagination):
    default_limit = 100
    max_limit = 100


class BookDetailsView(APIView):
    """
    API to get book details
    """
    authentication_classes = (BearerAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        volume_id = request.GET.get('volume_id')
        try:
            book_model = BooksDataExtractor().search_books_by_volume_id(volume_id)
            # book = Book.objects.filter(volume_id=volume_id).first()
            # serializer = BookSerializer(book, many=False)
            return JsonResponse(book_model, safe=False)
        except Exception as e:
            raise Exception(str(e))


class SearchBookItems(APIView):
    pagination_class = Paginator
    renderer_classes = [renderers.JSONRenderer]
    authentication_classes = (BearerAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        try:
            result_set = self.get_queryset()
            if result_set:
                return Response(result_set, status.HTTP_200_OK)
            return Response('Server not responding! Please try after some time', status.HTTP_404_NOT_FOUND)
        except Exception as e:
            additional_message = f'{args}, {kwargs}, {request.data}, {request.GET}'
            traceback.print_exc()
            raise APIException(f'{str(e)}, additional_message: {additional_message}')

    def get_queryset(self):
        query_dict = self._get_query_dict()
        # query_set = self._get_query_result(query_dict)
        return self._memoize_if_query_set_is_empty(query_dict)

    # def get_serializer_class(self):
    #     return BookSerializer

    def _get_query_dict(self):
        serializer = SearchBookQuerySerializer(data=self.request.query_params)
        serializer.is_valid(raise_exception=True)
        query_dict = self.request.query_params.dict()
        return query_dict

    def _get_query_result(self, query_dict):
        search_str = query_dict['query']
        return Book.objects.filter(title__icontains=search_str)

    def _memoize_if_query_set_is_empty(self, query_dict):
        # if query_set:
        #     return query_set
        search_str = query_dict['query']
        book_res_set = BooksDataExtractor().search_books_by_name(search_str)
        # query_res = self._get_query_result(query_dict)
        return book_res_set


class BookRatings(ListAPIView):
    pagination_class = Paginator
    renderer_classes = [renderers.JSONRenderer]
    authentication_classes = (BearerAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        try:
            return self.list(request, *args, **kwargs)
        except Exception as e:
            additional_message = f'{args}, {kwargs}, {request.data}, {request.GET}'
            traceback.print_exc()
            raise APIException(f'{str(e)}, additional_message: {additional_message}')

    def _get_query_dict(self):
        query_dict = self.request.query_params.dict()
        return query_dict

    def get_queryset(self):
        query_dict = self._get_query_dict()
        volume_id = query_dict['volume_id']
        query_set = UserBookRatingReviews.objects \
            .filter(book__volume_id=volume_id) \
            .exclude(ratings__isnull=True, reviews__isnull=True) \
            .order_by('updated_at')
        return query_set

    def get_serializer_class(self):
        return BookRatingsSerializer


class SaveBookInListView(APIView):
    """
    This class has methods to save book into types of lists
    and to get books in the any type of list
    """
    authentication_classes = (BearerAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        user = request.user
        list_type = request.GET.get('list_type')
        try:
            user_list_obj = UserList.objects.filter(user=user, list=list_type).first()
            book_list = user_list_obj.book.all()
            result_set = self.create_list_of_books_with_author_details(book_list)
            print('@@@@@@@@@@@@@@@@@@@@@@@', result_set)
            return Response({'result': result_set}, status.HTTP_200_OK)
        except Exception as e:
            raise Exception(str(e))

    def post(self, request, *args, **kwargs):
        volume_id = request.data.get('volume_id')
        list_type = request.data.get('list_type')
        user = request.user
        try:
            with transaction.atomic():

                book = self.fetch_book_data_and_save_to_model(volume_id)
                user_list_object, created = UserList.objects.get_or_create(user=user, list=list_type)
                user_list_object.book.add(book.id)
                user_list_object.save()
                return Response({'message': 'Book successfully added!'}, status.HTTP_200_OK)
        except Exception as e:
            raise Exception(str(e))

    def fetch_book_data_and_save_to_model(self, volume_id):
        book = Book.objects.filter(volume_id=volume_id).first()
        if book:
            return book
        book_info_dict = BooksDataExtractor().search_books_by_volume_id(volume_id)
        book_obj = BODOAdapter().adapt_to_book_model(book_info_dict)
        return book_obj

    def create_list_of_books_with_author_details(self, book_set):
        """
        method to convert iterable query_set to list of dictionary
        format having all book details and respective author details
        """
        list_of_books = list()
        temp_book = dict()
        for book in book_set:
            temp_book['volume_id'] = book.volume_id
            temp_book['title'] = book.title
            temp_book['publish_date'] = book.publish_date
            temp_book['description'] = book.description
            temp_book['authors'] = book.authors.all().values()
            list_of_books.append(temp_book)
        return list_of_books
