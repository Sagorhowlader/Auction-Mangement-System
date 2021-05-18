from django.urls import path, include
from .views import *
urlpatterns = [

    path('',AuctionSite,name='AuctionSite'),
    path('createpost/',CreatePost,name='createpost'),
    path('<pk>/postview/',PostView.as_view(),name='postview'),
    path('liked/',like_unlike_post,name='postlike')
]
