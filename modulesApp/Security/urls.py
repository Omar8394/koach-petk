from django.urls import path, include  # add this
from modulesApp.Security.views import login,login_view,register_view,logout_view
app_name = "security"
urlpatterns = [
    path("login/", login_view, name="login"),
    path("register/", register_view, name="register"),
    path("logout/", logout_view, name="logout")

]
