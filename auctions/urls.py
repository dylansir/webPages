from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("viewListing", views.viewListing, name="viewListing"),
    path("bidPlace", views.bidPlace, name="bidPlace"),
    path("submitListing", views.submitListing, name="submitListing"),
    path("nameTaken", views.submitListing, name="nameTaken"),
    path("watchlist", views.watchlist, name="watchlist")
]
 