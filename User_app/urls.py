from django.urls import path
# ---
from .Profile.views import ShowUserProfileView, UpdateUserProfileView
from .Authentication.views import (UserRegistrationView, UsersForgotPasswordView, UsersForgotPasswordCheckOTPView)
from .Authentication.views import (UsersResetPasswordView, LoginUserView)

app_name = "User_app"
urlpatterns = [
    path('user-register/', UserRegistrationView.as_view()),
    path('user-login/', LoginUserView.as_view()),
    path('forget-password/', UsersForgotPasswordView.as_view()),
    path('check-token/', UsersForgotPasswordCheckOTPView.as_view()),
    path('reset-password/', UsersResetPasswordView.as_view()),
    path('show-profile/', ShowUserProfileView.as_view()),
    path('update-profile/', UpdateUserProfileView.as_view()),
]