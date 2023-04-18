
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("sharePost", views.sharePost, name="sharePost"),
    path("profile/<int:id>", views.profile, name="profile"),

    # API Routes
    path("followers/<int:id>", views.show_follower, name="show"),
    path("followUser/<int:id>", views.follow, name="follow"),
    path("unFollow/<int:id>", views.unFollow, name="unFollow"),

    
]
