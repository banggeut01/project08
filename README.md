# 08 - REST API

## 1. 목표

* API 요청에 대한 이해
* RESTful API 서버 구축
* API 문서화

## 2. 준비 사항

1. **(필수)** Python Web Framework
   * Django 2.2.x
   * Python 3.7.x

## 3. 요구 사항

1. **데이터베이스 설계**

   * `db.sqlite3`에서 테이블 간의 관계는 아래와 같습니다.

   * `movies_movies`

     | 필드명      | 자료형  | 설명                      |
     | ----------- | ------- | ------------------------- |
     | id          | Integer | Primary Key               |
     | title       | String  | 영화명                    |
     | audience    | Integer | 누적 관객수               |
     | poster_url  | String  | 포스터 이미지 URL         |
     | description | Text    | 영화 소개                 |
     | genre_id    | Integer | Genre의 Primary Key(id값) |

   * `movies_genres`

     | 필드명 | 자료형  | 설명        |
     | ------ | ------- | ----------- |
     | id     | Integer | Primary Key |
     | name   | String  | 장르 구분   |

   * `movies_reviews`

     | 필드명   | 자료형  | 설명                       |
     | -------- | ------- | -------------------------- |
     | id       | Integer | Primary Key                |
     | content  | String  | 한줄평(평가 내용)          |
     | score    | Integer | 평점                       |
     | movie_id | Integer | Movie의 Primary Key(id 값) |
     | user_id  | Integer | User의 Primary Key(id 값)  |

2. **Seed Data** 반영

   1. 주어진 `movie.json`과 `genre.json`을 `movies/fixtures/` 디렉토리로 옮깁니다.

   2. 아래의 명령어를 통해 반영합니다.

      ```shell
      $ python manage.py loaddata genre.json
      Installed 11 object(s) from 1 fixture(s)
      $ python manage.py loaddata movie.json
      Installed 10 object(s) from 1 fixture(s)
      ```

   3. `admin.py`에 `Genre`와 `Movie` 클래스를 등록한 후, `/admin`을 통해 실제로 데이터베이스에 반영되었는지 확인해봅시다.

3. `movies` API

   * 아래와 같은 API 요청을 보낼 수 있는 서버를 구축해야 합니다.

   * 허용된 HTTP 요청을 제외하고는 모두 405 Method Not Allowed를 응답합니다.

   * `movies/models.py`

     ```python
     from django.db import models
     from django.conf import settings
     
     class Genre(models.Model):
         name = models.CharField(max_length=20)
     
     class Movie(models.Model):
         title = models.CharField(max_length=20)
         audience = models.IntegerField()
         poster_url = models.CharField(max_length=50)
         description = models.TextField()
         genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
     
     class Review(models.Model):
         content = models.CharField(max_length=50)
         score = models.IntegerField()
         movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
     ```

   * `urls.py`

     ```python
     from django.contrib import admin
     from django.urls import path, include
     
     urlpatterns = [
         path('admin/', admin.site.urls),
         path('api/v1/', include('movies.urls')),
     ]
     ```

   * `movies/urls.py`

     ```python
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
     
     ```

   * `movies.serializers.py`

     ```python
     from rest_framework import serializers
     from .models import Genre, Movie, Review
     
     class GenreSerializers(serializers.ModelSerializer):
         class Meta:
             model = Genre
             fields = ['id', 'name']
             
     class MovieSerializers(serializers.ModelSerializer):
         class Meta:
             model = Movie
             fields = ['id', 'title', 'audience', 'poster_url', 'description', 'genre']
     
     class GenreDetailSerializers(serializers.ModelSerializer):
         movie_set = MovieSerializers(many=True)
         class Meta(GenreSerializers.Meta):
             fields = GenreSerializers.Meta.fields + ['movie_set',]
     
     class ReviewSerializers(serializers.ModelSerializer):
         class Meta:
             model = Review
             fields = ('id', 'content', 'score')
     ```

   * `movies/views.py`

     1. `GET /api/v1/genres/`

        ```python
        from django.shortcuts import render, get_object_or_404
        from rest_framework.response import Response
        from rest_framework.decorators import api_view
        from . models import Genre, Movie, Review
        from .serializers import GenreSerializers, MovieSerializers, GenreDetailSerializers, ReviewSerializers
        
        @api_view(['GET'])
        def genre_index(request):
            genres = Genre.objects.all()
            serializer = GenreSerializers(genres, many=True)
            return Response(serializer.data)
        ```

        

     2. `GET /api/v1/genres/{genre_pk}/`

        ```python
        @api_view(['GET'])
        def genre_detail(request, genre_pk):
            genre = get_object_or_404(Genre, pk=genre_pk)
            serializer = GenreDetailSerializers(genre)
            return Response(serializer.data)
        ```

        

     3. `GET /api/v1/movies/`

        ```python
        @api_view(['GET'])
        def movie_index(request):
            movies = Movie.objects.all()
            serializer = MovieSerializers(movies, many=True)
            return Response(serializer.data)
        ```

        

     4. `GET /api/v1/movies/{movie_pk}/`

        ```python
        @api_view(['GET'])
        def movie_detail(request, movie_pk):
            movie = get_object_or_404(Movie, pk=movie_pk)
            serializer = MovieSerializers(movie)
            return Response(serializer.data)
        ```

        

     5. `POST /api/v1/movies/{movie_pk}/reviews/`

        ```python
        @api_view(['POST'])
        def create_review(request, movie_pk):
            movie = get_object_or_404(Movie, pk=movie_pk)
            serializer = ReviewSerializers(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save(movie_id=movie_pk)
            return Response({'message': '작성되었습니다.'})
        ```

        

     6. `PUT /api/1/reviews/{review_pk}/`, `DELETE /api/v1/reviews/{review_pk}/`

        ```python
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
        ```

        

## 4. API documents

* `GET /api/v1/genres/`

  ![genre_index](./images/genre_index.jpg)

* `GET /api/v1/genres/{genre_pk}/`

  * 올바른 genre_pk로 접근하였을 때

  ![genre_detail](./images/genre_detail.jpg)

  * 존재하지 않는 genre_pk일 때

    ![genre_detail](./images/genre_detail_404.jpg)

* `GET /api/v1/movies/`

  ![movie_index](./images/movie_index.jpg)

* `GET /api/v1/movies/{movie_pk}/`

  ![movie_detail](./images/movie_detail.jpg)

* `POST /api/v1/movies/{movie_pk}/reviews/`

  * GET 방법이 아닌 POST, PUT, DELETE 방법은 `postman`툴을 사용하여 확인하였습니다.
  * [postman 링크](https://www.getpostman.com/)

  ![review_create](./images/review_create.jpg)

  * admin 페이지에서 review가 생성된 것을 확인할 수 있습니다.

  ![review_admin](./images/review_create_admin.jpg)

* `PUT /api/1/reviews/{review_pk}/`

  ![review_update](./images/review_update.jpg)

  * admin 페이지에서 review가 수정된 것을 확인할 수 있습니다.

  ![review_update](./images/review_update_admin.jpg)

* `DELETE /api/v1/reviews/{review_pk}/`

  ![review_delete](./images/review_delete.jpg)

  * admin 페이지를 통해 review가 삭제 된 것을 확인할 수 있습니다.

  ![review_delete_admin](./images/review_delete_admin.jpg)