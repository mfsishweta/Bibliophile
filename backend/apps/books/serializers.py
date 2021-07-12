from apps.feedbacks.models import UserBookRatingReviews
from rest_framework import serializers


class BookRatingsSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username')

    class Meta:
        model = UserBookRatingReviews
        fields = ('user_name', 'ratings', 'reviews')
