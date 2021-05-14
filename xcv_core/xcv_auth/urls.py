from django.urls import path
from .views import login_request, logout_request
from .views import HomeView, ChangePasswordView

app_name = 'xcv_auth'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('login/', login_request, name='login'),
    path('logout/', logout_request, name='logout'),
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),
]
