from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),

    path('signup', views.signup, name='signup'),
    path('signin', views.signin, name='signin'),
    path('logout', views.logout, name='logout'),

    path('settings', views.settings, name='settings'),
    path('upload', views.upload, name='upload'),
    
    path('add_to_wishList/<str:postid>', views.add_to_wishList, name='add_to_wishList'),
    path('wishList', views.wishList, name='wishList'),


    # path('search', views.search, name='search'),
    path('inforpage/<str:postid>', views.inforpage, name='inforpage'),
    path('like-post', views.like_post, name='like-post'),

    # path('addToWishList/<uid>/', views.addToWishList, name='add_to_wishlist')


]
