from django.urls import path
from movies import views

app_name = 'movies'

urlpatterns = [
    path('', views.list_movie, name='list-movie'),
    path('api/genre', views.genre_autocomplete, name='genre-autocomplete'),
    path('api/rating', views.rating_autocomplete, name='rating-autocomplete'),
    path('detail/<int:id>/<str:name>', views.detail_movie, name='detail-movie'),
    path('movies', views.movies, name='movies'),
    path('create-movie', views.create_movie, name='create-movie'),
    path('update-movie/<int:id>', views.update_movie, name='update-movie'),
    path('delete-movie/<int:id>', views.delete_movie, name='delete-movie'),
    path('list-genre', views.list_genre, name='list-genre'),
    path('delete-genre/<int:id>', views.delete_genre, name='delete-genre'),
    path('list-mpaa-rating', views.list_mpaa_rating, name='list-mpaa-rating'),
    path('delete-mpaa-rating/<int:id>', views.delete_mpaa_rating, name='delete-mpaa-rating')
]
