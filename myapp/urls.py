from django.urls import path
from .import views
app_name = 'myapp'
urlpatterns = [
    path('', views.home, name='home'),
    path('newsearch/', views.new_search, name='newsearch'),
]