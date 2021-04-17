from django.urls import path
from .views import SignUpView, renderAccountView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('user/', renderAccountView, name='account'),
]
