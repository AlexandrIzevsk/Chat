from django.urls import path
from .views import SignUp, confirm_signup, ProfileView
from django.contrib.auth.views import LoginView, LogoutView


urlpatterns = [
    path('signup/', SignUp.as_view(), name='signup'),
    path('login/', ProfileView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='registration/logout.html'), name='logout'),
    path('confirm_signup/', confirm_signup, name='confirm_signup'),
]
