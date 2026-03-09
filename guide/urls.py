from django.contrib.auth.views import LogoutView
from django.urls import path
from guide import views

app_name = 'guide'

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('accounts/register/', views.register, name='register'),
    path('accounts/login/', views.login_view, name='login'),
    path('accounts/logout/', LogoutView.as_view(), name='logout'),
    path('posts/', views.post_list, name='post_list'),
    path('posts/new/', views.post_create, name='post_create'),
    path('posts/<int:pk>/like/', views.post_like, name='post_like'),
    path('posts/<int:pk>/save/', views.post_save, name='post_save'),
    path('posts/<int:pk>/', views.post_detail, name='post_detail'),
    path('collections/', views.collection_list, name='collection_list'),
    path('collections/new/', views.collection_create, name='collection_create'),
    path('collections/<int:collection_pk>/add/<int:post_pk>/', views.collection_add, name='collection_add'),
    path('collections/<int:collection_pk>/remove/<int:post_pk>/', views.collection_remove, name='collection_remove'),
    path('collections/<int:pk>/delete/', views.collection_delete, name='collection_delete'),
    path('collections/<int:pk>/', views.collection_detail, name='collection_detail'),
]
