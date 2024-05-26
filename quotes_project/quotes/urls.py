from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

from .forms import CustomPasswordResetForm, CustomSetPasswordForm

app_name = 'quotes'

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('add_author/', views.add_author, name='add_author'),
    path('add_quote/', views.add_quote, name='add_quote'),
    path('tag/<str:tag>/', views.quotes_by_tag, name='quotes_by_tag'),
    path('scrap_quotes/', views.scrap_quotes, name='scrap_quotes'),
    path('password_reset/', auth_views.PasswordResetView.as_view(form_class=CustomPasswordResetForm),
         name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(form_class=CustomSetPasswordForm),
         name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

]
