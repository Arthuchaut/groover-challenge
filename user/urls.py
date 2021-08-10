from django.urls import path
from .views import AuthCallbackView, AuthView

app_name: str = 'user'
urlpatterns = [
    path('', AuthView.as_view(), name='auth'),
    path('callback/', AuthCallbackView.as_view(), name='auth_callback'),
]
