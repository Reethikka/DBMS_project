from django.urls import path

from . import views

app_name="polls"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("<int:pk>/",views.DetailView.as_view(),name="detail"),
    path("<int:pk>/results/",views.ResultsView.as_view(),name="results"),
    path("<int:question_id>/vote/",views.vote,name="vote"),
    path("about/",views.about,name="about"),
    path("login/", views.login_page, name='login'),
    path("register/", views.register_page, name='register'),
    path("logout/", views.logout_page, name='logout'),
]
