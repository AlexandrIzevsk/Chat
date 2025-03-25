from django.urls import include, path
from .views import Profile, ListChats
from rest_framework import routers
from . import views


router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'chat', views.ChatViewSet)
router.register(r'message', views.MessageViewSet)


urlpatterns = [
    # path('profile/', Profile.as_view(), name='profile'),
    path('', ListChats.as_view(), name='chats'),
    path('api/', include(router.urls), name='api'),
    path('profile/', views.EditProfileView.as_view(), name='profile'),
]