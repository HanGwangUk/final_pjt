from django.urls import path
from . import views

app_name = "movies"

urlpatterns=[
    path('', views.index, name="index"),
    path('<int:movie_pk>/', views.detail, name='detail'),
    path('<int:movie_pk>/rank/', views.rank, name='rank'),
    path('<int:movie_pk>/review_create/', views.review_create, name='review_create'),
    path('<int:movie_pk>/<int:review_pk>/', views.review_detail, name='review_detail'),
    path('<int:movie_pk>/<int:review_pk>/update', views.review_update, name='review_update'),
    path('<int:movie_pk>/<int:review_pk>/delete', views.review_delete, name='review_delete'),
    path('<int:movie_pk>/<int:review_pk>/comments', views.comment_create, name='comment_create'),
    path('<int:movie_pk>/<int:review_pk>/<int:comment_pk>/comment_delete', views.comment_delete, name='comment_delete'),
    # path('<int:movie_pk>/rank', views.rank, name='rank')

]