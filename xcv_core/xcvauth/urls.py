from django.urls import path
from .views import home, login_request, logout_request, ChangePasswordView

app_name = 'xcvauth'

urlpatterns = [
    path('', home, name='home'),
    path('login/', login_request, name='login'),
    path('logout/', logout_request, name='logout'),
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),
]
