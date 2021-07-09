import traceback

# Create your views here.
from apps.books.google_book_data_storage import BooksDataExtractor
from apps.books.models import Book
from apps.books.serializers import BookRatingsSerializer
from apps.feedbacks.models import UserBookRatingReviews
from django.db import transaction
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from rest_framework import renderers, serializers
from rest_framework.exceptions import APIException
from rest_framework.generics import ListAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.views import APIView


class Paginator(LimitOffsetPagination):
    default_limit = 100
    max_limit = 100


class BookDetailsView(APIView):
    """
    API to get book details
    """

    def get(self, request, volume_id):
        try:
            book = Book.objects.filter(volume_id=volume_id).first()
            serializer = BookSerializer(book, many=False)
            return JsonResponse(serializer.data, safe=False)
        except Exception as e:
            raise APIException(str(e))


class SearchBookQuerySerializer(serializers.Serializer):
    q = serializers.CharField(max_length=100, required=True)

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


@method_decorator(transaction.non_atomic_requests, name='dispatch')
class SearchBookItems(ListAPIView):
    pagination_class = Paginator
    renderer_classes = [renderers.JSONRenderer]

    def get(self, request, *args, **kwargs):
        try:
            return self.list(request, *args, **kwargs)
        except Exception as e:
            additional_message = f'{args}, {kwargs}, {request.data}, {request.GET}'
            traceback.print_exc()
            raise APIException(f'{str(e)}, additional_message: {additional_message}')

    def get_queryset(self):
        query_dict = self._get_query_dict()
        query_set = self._get_query_result(query_dict)
        return self._memoize_if_query_set_is_empty(query_set, query_dict)

    def get_serializer_class(self):
        return BookSerializer

    def _get_query_dict(self):
        serializer = SearchBookQuerySerializer(data=self.request.query_params)
        serializer.is_valid(raise_exception=True)
        query_dict = self.request.query_params.dict()
        return query_dict

    def _get_query_result(self, query_dict):
        search_str = query_dict['q']
        return Book.objects.filter(title__icontains=search_str)

    def _memoize_if_query_set_is_empty(self, query_set, query_dict):
        if query_set:
            return query_set
        search_str = query_dict['q']
        BooksDataExtractor().search_books(search_str)
        query_res = self._get_query_result(query_dict)
        return query_res


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('id', 'title', 'description', 'authors', 'publish_date', 'volume_id')


class BookRatings(ListAPIView):
    pagination_class = Paginator
    renderer_classes = [renderers.JSONRenderer]

    def get(self, request, *args, **kwargs):
        try:
            return self.list(request, *args, **kwargs)
        except Exception as e:
            additional_message = f'{args}, {kwargs}, {request.data}, {request.GET}'
            traceback.print_exc()
            raise APIException(f'{str(e)}, additional_message: {additional_message}')

    def _get_query_dict(self):
        # serializer = SearchBookQuerySerializer(data=self.request.query_params)
        # serializer.is_valid(raise_exception=True)
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

