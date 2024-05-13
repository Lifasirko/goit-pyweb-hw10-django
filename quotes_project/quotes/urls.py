from django.urls import path
from . import views

app_name = 'quotes'

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('add_author/', views.add_author, name='add_author'),
    path('add_quote/', views.add_quote, name='add_quote'),
    path('tag/<str:tag>/', views.quotes_by_tag, name='quotes_by_tag'),
    path('scrap_quotes/', views.scrap_quotes, name='scrap_quotes'),
]
