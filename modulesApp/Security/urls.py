from django.urls import path, include  # add this
from modulesApp.Security.views import login,login_view,register_view,logout_view,changePassword,\
securitySettings,changeSecretQuestion,recovery_method, recovery_method_question,forgot_password
app_name = "security"
urlpatterns = [
    path("login/", login_view, name="login"),
    path("register/", register_view, name="register"),
    path("logout/", logout_view, name="logout"),
    path("changePassword/", changePassword, name="changePassword"),
    path("changeSecretQuestion/", changeSecretQuestion, name="changeSecretQuestion"),
    path("securitySettings/", securitySettings, name="securitySettings"),
    path("recoverymethod/", recovery_method, name="recovery_method"),
    path("recovery_method_question/", recovery_method_question, name="recovery_method_question"),
    path("forgotpassword/", forgot_password, name="forgot_password"),
    
    
    

]
