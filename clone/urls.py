from . import views
from django.urls import path
from django.contrib.auth import views as auth_views
from clone.views import CustomLoginView  
from clone.forms import LoginForm
from .views import profile



urlpatterns = [
    path('', views.home, name='users-home'),
    path('photo/<str:pk>/', views.viewPhoto, name='photo'),
	path('add/', views.addPhoto, name='add'),
    path('register/', views.RegisterView.as_view(), name='users-register'),
    path('login/', CustomLoginView.as_view(redirect_authenticated_user=True, template_name='auth/login.html',
                                           authentication_form=LoginForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='auth/logout.html'), name='logout'), 
    path('profile/', views.profile, name='users-profile'),
]