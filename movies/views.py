from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from . models import Genre, Movie, Review
from .serializers import GenreSerializers, MovieSerializers, GenreDetailSerializers, ReviewSerializers

# Create your views here.
@api_view(['GET'])
def genre_index(request):
    genres = Genre.objects.all()
    serializer = GenreSerializers(genres, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def genre_detail(request, genre_pk):
    genre = get_object_or_404(Genre, pk=genre_pk)
    serializer = GenreDetailSerializers(genre)
    return Response(serializer.data)

@api_view(['GET'])
def movie_index(request):
    movies = Movie.objects.all()
    serializer = MovieSerializers(movies, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def movie_detail(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    serializer = MovieSerializers(movie)
    return Response(serializer.data)

@api_view(['POST'])
def create_review(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    serializer = ReviewSerializers(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(movie_id=movie_pk)
    return Response({'message': '작성되었습니다.'})

@api_view(['PUT', 'DELETE'])
def update_delete_review(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    if request.method == 'PUT':
        serializer = ReviewSerializers(data=request.data, instance=review)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'message': '수정되었습니다.'})
    else: # delete
        review.delete()
        return Response({'message': '삭제되었습니다.'})
