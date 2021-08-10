from django.urls import path
from .views import AuthView, AuthRefreshTokenView, AuthCallbackView

app_name: str = 'user'
urlpatterns = [
    path('', AuthView.as_view(), name='auth'),
    path(
        'refresh-token/',
        AuthRefreshTokenView.as_view(),
        name='auth_refresh_token',
    ),
    path('callback/', AuthCallbackView.as_view(), name='auth_callback'),
]
