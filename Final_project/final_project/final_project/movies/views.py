from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
from django.db.models import Q

#Create your views here.
def rank(request, movie_pk):
    movie = get_object_or_404(Movie, pk = movie_pk)
    rate = Rate.objects.all()
    total = (movie.vote_average) * (movie.vote_count)
    if request.user.is_authenticated:
        if request.user not in movie.vote_user.all():
            form = RatingForm(request.POST)
            if form.is_valid():
                rate = form.save(commit=False)
                rate.user = request.user
                rate.movie = movie
                rate.save()
                movie.vote_user.add(request.user)
    
    return redirect('movies:detail', movie.pk)


def index(request):
    movies = Movie.objects.all()
    fr_movies = Movie.objects.all().filter(original_language = 'ko').order_by('?')[:21]
    en_movies = Movie.objects.all().filter(~Q(original_language = 'ko'), vote_average__gte=1).order_by('?')[:21]

    
    context = {
        'movies' : movies,
        'fr_movies': fr_movies,
        'en_movies': en_movies
    }
    return render(request, 'movies/index.html', context)

def detail(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    genre = Genre.objects.all()
    rate = Rate.objects.all()
    form = RatingForm(request.POST)
    total = (movie.vote_average) * (movie.vote_count)
    context = {
        'movie':movie,
        'genre':genre,
        'total':total,
        'rate' : rate,
        'form': form,
        
    }
    return render(request, 'movies/detail.html', context)

@login_required
def review_create(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.movie = movie
            review.user = request.user
            review.save()
            return redirect('movies:review_detail', review.movie.id, review.pk)
    else:
        form = ReviewForm()
    context = {
        'form': form,
        'movie':movie
    }
    return render(request, 'movies/review_form.html', context)


def review_detail(request, movie_pk, review_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    review = get_object_or_404(Review, pk=review_pk)
    form = CommentForm()

    context = {
        'movie':movie,
        'review' : review,
        'form':form
    }
    return render(request, 'movies/review_detail.html', context)

@login_required
def review_update(request, movie_pk, review_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    review = get_object_or_404(Review, pk=review_pk)
    # 글작성 유저랑 로그인 한 유저가 같을 때
    if request.user == review.user:
        # POST방식일 때
        if request.method == "POST":
            form = ReviewForm(request.POST, instance=review)
            if form.is_valid():
                review = form.save(commit=False)
                review.user = request.user
                review.movie = movie
                review.save()
                # 글수정을 완료하고 review_detail페이지로 돌려줌
                return redirect('movies:review_detail', review.movie.id, review.pk)
        # GET방식일때
        else:
            form = ReviewForm(instance=review)
        context = {
            'form':form,
        }
        return render(request, 'movies/review_form.html', context)
    else:
        return redirect('movies:review_detail', review_pk, movie_pk)

@login_required
@require_POST
def review_delete(request, movie_pk, review_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    review = get_object_or_404(Review, pk=review_pk )
    if request.user == review.user:
        review.delete()
    return redirect('movies:detail', movie.pk)

@require_POST
def comment_create(request, movie_pk, review_pk):
    if request.user.is_authenticated:
        movie = get_object_or_404(Movie, pk=movie_pk)
        review = get_object_or_404(Review, pk=review_pk)
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.review = review
            comment.save()
    return redirect('movies:review_detail', movie.pk, review.pk)

@login_required
@require_POST
def comment_delete(request, movie_pk, review_pk, comment_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    review = get_object_or_404(Review, pk=review_pk)
    comment = get_object_or_404(Comment, pk=comment_pk)
    if request.user == comment.user:
        comment.delete()  
    return redirect('movies:review_detail', movie.pk, review.pk)