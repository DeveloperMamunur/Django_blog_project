from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('detail-post/<str:slug>/', views.detail_post, name='detail_post'),
    # blog backend urls
    path('backend/dashboard/', views.dashboard, name='dashboard'),
    # blog category urls
    path('backend/category/', views.category_list, name='category_list'),
    path('backend/category/update/<int:id>/', views.category_update, name='category_update'),
    path('backend/category_delete/<int:id>/', views.category_delete, name='category_delete'),
    path('backend/category/category_inactive/<int:id>/', views.category_inactive, name='category_inactive'),
    path('backend/category/category_active/<int:id>/', views.category_active, name='category_active'),
    # blog tags urls
    path('backend/tags/', views.tags_list, name='tags_list'),
    path('backend/tags/update/<int:id>/', views.tags_update, name='tags_update'),
    path('backend/tags_delete/<int:id>/', views.tags_delete, name='tags_delete'),
    path('backend/tags/tags_inactive/<int:id>/', views.tags_inactive, name='tags_inactive'),
    path('backend/tags/tags_active/<int:id>/', views.tags_active, name='tags_active'),
    # blog post urls
    path('backend/post/', views.post_list, name='post_list'),
    path('backend/post/create/', views.post_create, name='post_create'),
    path("backend/post/update/<int:id>/", views.post_update, name="post_update"),
    path("backend/post/delete/<int:id>/", views.post_delete, name="post_delete"),
    path("backend/post/post_inactive/<int:id>/", views.post_inactive, name="post_inactive"),
    path("backend/post/post_active/<int:id>/", views.post_active, name="post_active"),
    path('backend/post/details/<int:id>/', views.post_details, name='post_details'),
    path('backend/post/details/active/<int:id>/', views.post_active_details, name='post_active_details'),
    path('backend/post/details/inactive/<int:id>/', views.post_inactive_details, name='post_inactive_details'),
    path('backend/post/details/delete/<int:id>/', views.post_delete_details, name='post_delete_details'),
    path('backend/post/published/<int:id>/', views.post_published, name='post_published'),
    path('backend/post/unpublished/<int:id>/', views.post_unpublished, name='post_unpublished'),
    # comments urls
    path('detail-post/comment/<str:slug>/', views.post_comment, name='post_comment'),
]
