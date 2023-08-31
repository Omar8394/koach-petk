from django.urls import path, include  # add this
from modulesApp.Security.views import login,login_view,register_view,logout_view,changePassword,\
securitySettings,changeSecretQuestion,recovery_method, recovery_method_question,forgot_password, \
account_recovery, testvue, testdata , editProfile, images, borrarImages, rootImages, renderListasCombos,verificationaccount, review_new_register,Modaltransfersec
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
    path("account_recovery/<str:activation_key>/",account_recovery , name="account_recovery"),
    path("testvue/", testvue, name="testvue"),
    path("testdata/", testdata, name="testdata"),
    path("editProfile/", editProfile, name='editProfile'),
    path("images/", images, name='images'),
    path("rootImages/", rootImages, name='rootImages'),
    path("borrarImages/", borrarImages, name='borrarImages'),
    path('renderListasCombos', renderListasCombos, name='renderListasCombos'),
    path("verificationaccount/<str:activation_key>/", verificationaccount, name="verification_account"),
    path('new_register', review_new_register, name='new_register'),
    path('Modaltransfersec', Modaltransfersec, name='Modaltransfersec'),
    
    

]
