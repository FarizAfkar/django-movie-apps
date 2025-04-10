from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse
from django.db.models import Q
from movies.forms import GenreForm, MPAA_RatingForm, MovieForm
from movies.models import Genre, MPAA_Rating, Movie, MovieGenre

# Check if the current user is a superuser
def is_superuser(user):
    """Decorator User Test."""
    return user.is_superuser

@login_required
@user_passes_test(is_superuser)
def rating_autocomplete(request):
    """API to return genre suggestions for autocomplete."""
    query = request.GET.get('term', '')
    ratings = MPAA_Rating.objects\
            .filter(
                Q(type_mpaa__icontains=query)|
                Q(label__icontains=query))[:5]
    suggestions = [{
            'label': f'{rating.type_mpaa}: {rating.label}',
            'value': rating.id
        }for rating in ratings]

    return JsonResponse(suggestions, safe=False)

@login_required
@user_passes_test(is_superuser)
def genre_autocomplete(request):
    """API to return genre suggestions for autocomplete."""
    query = request.GET.get('term', '')
    genres = Genre.objects.filter(name__icontains=query)[:5]
    suggestions = [{
            'label': genre.name,
            'value': genre.id
        }for genre in genres]

    return JsonResponse(suggestions, safe=False)

# Create your views here.
def list_movie(request):
    # Get Object Movie
    movies = Movie.objects.all().order_by('-userRating')

    # Pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(movies, 8)

    try:
        movies = paginator.page(page)
    except PageNotAnInteger :
        movies = paginator.page(1)
    except EmptyPage:
        movies = paginator.page(paginator.num_pages)

    # Render Context to HTML
    context = {
        'movies': movies
    }

    return render(request, 'movies/index.html', context)

def detail_movie(request, id, name):
    # Get Object Movie
    try:
        movie = Movie.objects.get(id=id, name=name)
        movie_genre = MovieGenre.objects.filter(movie_id=id)\
                    .values_list('genre__name', flat=True)

    except Exception as e:
        print('Error : ', e)
        raise PermissionDenied

    # Render Context to HTML
    context = {
        'movie': movie,
        'movie_genre': movie_genre
    }

    return render(request, 'movies/detail.html', context)

@login_required
@user_passes_test(is_superuser)
def movies(request):
    # Get Object Movie
    movies = Movie.objects.all().order_by('name')

    # Get Search Param
    search= request.GET.get('search')
    if search:
        movies = movies.filter(name__icontains=search)

    # Pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(movies, 10)

    try:
        movies = paginator.page(page)
    except PageNotAnInteger :
        movies = paginator.page(1)
    except EmptyPage:
        movies = paginator.page(paginator.num_pages)

    # Render Context to HTML
    context = {
        'movies': movies
    }

    return render(request, 'movies/list_movie.html', context)

@login_required
@user_passes_test(is_superuser)
def create_movie(request):
    # Set Form Create
    form_movie = MovieForm(request.POST)

    # Request Post Create
    if request.method == 'POST' and request.POST['btn_action'] == 'create_movie':

        # Create Movie
        movie = Movie.objects.create(
            name = request.POST['name'],
            description = request.POST['description'],
            imgPath = request.FILES['imgPath'],
            duration = request.POST['duration'],
            language = request.POST['language'],
            userRating = request.POST['userRating'],
            mpaaRating = MPAA_Rating.objects.get(id=request.POST['mpaaRating']),
        )

        # Create Movie Genre
        for genre in request.POST.getlist('genre'):
            MovieGenre.objects.create(
                movie = movie,
                genre = Genre.objects.get(id=genre)
            )

        # Message Toast
        messages.success(request, 'Movie has been successfully added!')

        return redirect('movies:create-movie')

    # Render Context to HTML
    context = {
        'form_movie': form_movie
    }

    return render(request, 'movies/add_movie.html', context)

@login_required
@user_passes_test(is_superuser)
def update_movie(request, id):
    # Get Object Movie
    try:
        movie = Movie.objects.get(id=id)
        movie_genre = MovieGenre.objects.filter(movie_id=id)

    except Exception as e:
        print('Error : ', e)
        raise PermissionDenied

    # Set Form Update
    form_movie = MovieForm(instance=movie)

    # Request Post Update
    if request.method == 'POST' and request.POST['btn_action'] == 'update_movie':

        # Update Movie
        movie.name = request.POST['name']
        movie.description = request.POST['description']
        movie.duration = request.POST['duration']
        movie.language = request.POST['language']
        movie.userRating = request.POST['userRating']
        movie.mpaaRating = MPAA_Rating.objects.get(id=request.POST['mpaaRating'])

        # Check File Poster
        if request.FILES:
            movie.imgPath = request.FILES['imgPath']

        # Save to DB
        movie.save()

        # Delete Unique Together to simplyfy
        movie_genre.delete()

        # Create Movie Genre
        for genre in request.POST.getlist('genre'):
            MovieGenre.objects.create(
                movie = movie,
                genre = Genre.objects.get(id=genre)
            )

        # Message Toast
        messages.info(request, 'Movie has been updated successfully!')

        return redirect('movies:update-movie', id=id)

    # Render Context to HTML
    context = {
        'movie': movie,
        'movie_genre': movie_genre,
        'form_movie': form_movie
    }

    return render(request, 'movies/update_movie.html', context)

@login_required
@user_passes_test(is_superuser)
def delete_movie(request, id):
    # Get Object Movie
    try:
        MovieGenre.objects.filter(movie_id=id).delete()
        Movie.objects.get(id=id).delete()

        # Message Toast
        messages.info(request, 'Movie has been deleted successfully!')

    except Exception as e:
        print('Error : ', e)
        raise PermissionDenied

    return redirect('movies:movies')

@login_required
@user_passes_test(is_superuser)
def list_genre(request):
    # Get Object Genre
    list_genre = Genre.objects.all().order_by('name')

    # Get Search Param
    search= request.GET.get('search')
    if search:
        list_genre = list_genre.filter(name__icontains=search)

    # Set Form Create
    form_create = GenreForm(request.POST)

    # Pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(list_genre, 10)

    try:
        list_genre = paginator.page(page)
    except PageNotAnInteger :
        list_genre = paginator.page(1)
    except EmptyPage:
        list_genre = paginator.page(paginator.num_pages)

    # Request Post Create
    if request.method == 'POST' and request.POST['btn_action'] == 'add_genre':

        # Validate Genre
        if form_create.is_valid():
            form_create.save()

            # Message Toast
            messages.success(request, 'Genre has been successfully added!')

            return redirect('movies:list-genre')

    # Request Post Update
    if request.method == 'POST' and 'update_genre' in request.POST['btn_action']:

        # Validate Genre
        id = request.POST['btn_action'].strip('update_genre_')
        update_data = request.POST[f'update_genre_{id}']

        # Get Object Genre
        try:
            genre = Genre.objects.get(id=id)
            genre.name = update_data
            genre.save()

            # Message Toast
            messages.info(request, 'Genre has been updated successfully!')

            return redirect('movies:list-genre')

        except Genre.DoesNotExist:
            raise PermissionDenied()

    # Render Context to HTML
    context = {
        'list_genre': list_genre,
        'form_create': form_create,
    }

    return render(request, 'movies/genre.html', context)

@login_required
@user_passes_test(is_superuser)
def delete_genre(request, id):
    # Get Object Genre
    try:
        genre = Genre.objects.get(id=id)
        genre.delete()

        # Message Toast
        messages.info(request, 'Genre has been deleted successfully!')

    except Genre.DoesNotExist:
        raise PermissionDenied()

    return redirect('movies:list-genre')

@login_required
@user_passes_test(is_superuser)
def list_mpaa_rating(request):
    # Get Object Rating
    list_rating = MPAA_Rating.objects.all().order_by('id')

    # Get Search Param
    search= request.GET.get('search')
    if search:
        list_rating = list_rating.filter(
            Q(type_mpaa__icontains=search)|Q(label__icontains=search))

    # Set Form Create
    form_create = MPAA_RatingForm(request.POST)

    # Pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(list_rating, 10)

    try:
        list_rating = paginator.page(page)
    except PageNotAnInteger :
        list_rating = paginator.page(1)
    except EmptyPage:
        list_rating = paginator.page(paginator.num_pages)

    # Request Post Create
    if request.method == 'POST' and request.POST['btn_action'] == 'add_mpaa_rating':

        # Validate Rating
        if form_create.is_valid():
            form_create.save()

            # Message Toast
            messages.success(request, 'MPAA Rating has been successfully added!')

            return redirect('movies:list-mpaa-rating')

    # Request Post Update
    if request.method == 'POST' and 'update_rating' in request.POST['btn_action']:

        # Validate Rating
        id = request.POST['btn_action'].strip('update_rating_')
        update_type = request.POST[f'update_rating_type_{id}']
        update_label = request.POST[f'update_rating_label_{id}']

        # Get Object Rating
        try:
            rating = MPAA_Rating.objects.get(id=id)
            rating.type_mpaa = update_type
            rating.label = update_label
            rating.save()

            # Message Toast
            messages.info(request, 'MPAA Rating has been updated successfully!')

            return redirect('movies:list-mpaa-rating')

        except Genre.DoesNotExist:
            raise PermissionDenied()

    # Render Context to HTML
    context = {
        'list_rating': list_rating,
        'form_create': form_create,
    }

    return render(request, 'movies/mpaa_rating.html', context)

@login_required
@user_passes_test(is_superuser)
def delete_mpaa_rating(request, id):
    # Get Object Rating
    try:
        genre = MPAA_Rating.objects.get(id=id)
        genre.delete()

        # Message Toast
        messages.info(request, 'MPAA Rating has been deleted successfully!')

    except MPAA_Rating.DoesNotExist:
        raise PermissionDenied()

    return redirect('movies:list-mpaa-rating')
