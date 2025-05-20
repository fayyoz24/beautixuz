# users/urls.py
from django.urls import path
from .views import SignupView, ConfirmPhoneView, LoginView

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('confirm-phone/', ConfirmPhoneView.as_view(), name='confirm-phone'),
    path('login/', LoginView.as_view(), name='token_obtain_pair'),
]
