from django.shortcuts import render, get_object_or_404
from .models import *
from .forms import *
from django.db.models import Q

# Create your views here.
def index(request):
    movies = Movie.objects.all()
    fr_movies = Movie.objects.all().filter(original_language = 'fr').order_by('?')[:20]
    en_movies = Movie.objects.all().filter(~Q(original_language = 'fr'), vote_average__gte=1).order_by('?')[:20]

    
    context ={
        'movies' : movies,
        'fr_movies': fr_movies,
        'en_movies': en_movies
    }
    return render(request, 'movies/index.html', context)

def detail(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    genre = Genre.objects.all()

    context = {
        'movie':movie,
        'genre':genre
    }
    return render(request, 'movies/detail.html', context)

def review_create(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.movie = movie
            review.user = request.user
            review.save()
            # return redirect('movies:review_detail')
    else:
        form = ReviewForm()
    context = {
        'form': form,
        'movie':movie
    }
    return render(request, 'movies/review_form.html', context)


