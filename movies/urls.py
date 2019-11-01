from django.urls import path
from . import views


urlpatterns = [
    path('genres/', views.genre_index, name='genre_index'),
    path('genres/<int:genre_pk>/', views.genre_detail, name='genre_detail'),
    path('movies/', views.movie_index, name='movie_index'),
    path('movies/<int:movie_pk>/', views.movie_detail, name='movie_detail'),
    path('movies/<int:movie_pk>/reviews/', views.create_review, name='create_review'),
    path('reviews/<int:review_pk>/', views.update_delete_review, name='update_delete_review'),
]
