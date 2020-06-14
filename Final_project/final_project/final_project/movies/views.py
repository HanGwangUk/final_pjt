from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import user_passes_test
from .models import *
from .forms import *
from django.db.models import Q
# 슈퍼유저인지 알아보기 위한 데코레이터

#Create your views here.
def rank(request, movie_pk):
    movie = get_object_or_404(Movie, pk = movie_pk)
    rate = Rate.objects.all()
    User = get_user_model()
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
        # else:
        #     rate.user = User.objects.get(id=request.user.id)
        #     a = Rate.objects.get(id=rate.user.id)
        #     a.delete()
        #     movie.vote_user.remove(request.user)
    return redirect('movies:detail', movie.pk)

def rank_cancle(request, movie_pk):
    movie = get_object_or_404(Movie, pk = movie_pk)
    rate = Rate.objects.all()
    rate.delete()
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
    rate = Rate.objects.all().filter(user_id=request.user.id)
    form = RatingForm(request.POST)
    genres = Genre.objects.all().filter(movie_genre=movie_pk)
    User = get_user_model()
    movie_names = Movie.objects.all().filter(vote_user=request.user.id)
    
    total = (movie.vote_average) * (movie.vote_count)
    # if request.user_id in rate:
    if movie_pk in rate:
        gname = movie.movie_genres.name
    else:
        gname = ""

    context = {
    'movie':movie,
    'genres':genres,
    'total':total,
    'rate' : rate,
    'form': form,
    'movie_names':movie_names
    # 'user_genre' : user_genre,
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

    ### 슈퍼유저인지 아닌지에 따른 영화 쓰기 ###
@user_passes_test(lambda u: u.is_superuser)
def movie_create(request):
    if request.method == "POST":
        form = MovieForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('movies:index')

    else:
        form = MovieForm()

    context = {
        'form' : form
    }
    return render(request, 'movies/m_cre_upd.html', context)

@user_passes_test(lambda u : u.is_superuser)
@login_required
def movie_delete(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    movie.delete()

    return redirect('movies:index')

@user_passes_test(lambda u: u.is_superuser)
@login_required
def movie_update(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    if request.method == 'POST':
        form = MovieForm(request.POST, instance=movie)
        if form.is_valid():
            form.save()
            return redirect('movies:index', movie_pk)
    else:
        form = MovieForm(instance=movie)
    context = {
        'form': form
    }
    return render(request, 'movies/m_cre_upd.html', context)