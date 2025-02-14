from django.urls import path
from . import views
from .views import MembershipExpiryDateView

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('membership-expiry/', MembershipExpiryDateView.as_view(), name='membership_expiry'),
]
