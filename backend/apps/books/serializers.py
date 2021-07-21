from apps.books.models import Book
from apps.feedbacks.models import UserBookRatingReviews
from rest_framework import serializers


class BookRatingsSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username')

    class Meta:
        model = UserBookRatingReviews
        fields = ('user_name', 'ratings', 'reviews')


class SearchBookQuerySerializer(serializers.Serializer):
    query = serializers.CharField(max_length=100, required=True)

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('id', 'title', 'description', 'authors', 'publish_date', 'volume_id')