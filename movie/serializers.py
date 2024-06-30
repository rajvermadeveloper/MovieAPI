from rest_framework import serializers
from .models import Movie,Review

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'

class MovieReviewSerializer(serializers.ModelSerializer):
    user=serializers.CharField(required=False)
    class Meta:
        model=Review
        fields = '__all__'

class MovieReviewUpdateSerializer(serializers.ModelSerializer):
    user=serializers.CharField(required=False)
    movie=serializers.CharField(required=False)
    class Meta:
        model=Review
        fields = '__all__'