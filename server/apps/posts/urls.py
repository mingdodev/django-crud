from django.urls import path

from server.apps.posts.views import *

urlpatterns = [
    path("", posts_list),
    # <str:> ...
    path("posts/<int:pk>",posts_read),
    path("posts/create", posts_create),
    path("posts/<int:pk>/delete", posts_delete),
    path("posts/<int:pk>/update", posts_update),
    path("posts/like",posts_like),
]

# primary key : 아이디랑 똑같다고 생각하기