from django.urls import path, re_path
from . import views

app_name = 'blog_app'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('blog_feed/', views.PostListView.as_view(), name='post_list'),
    path('drafts/', views.DraftListView.as_view(), name='draft_list'),
    re_path(r'^post/(?P<pk>\d+)/$', views.PostDetailView.as_view(), name='post_detail'),
    path('post/new/', views.create_post, name='post_new'),
    re_path(r'^post/(?P<pk>\d+)/edit/$', views.UpdatePost.as_view(), name='post_edit'),
    re_path(r'^post/(?P<pk>\d+)/delete/$', views.DeletePost.as_view(), name='post_delete'),
    re_path(r'^post/(?P<pk>\d+)/publish/$', views.publish_post, name='post_publish'),
    re_path(r'^post/(?P<pk>\d+)/comment/$', views.add_comment_to_post, name='post_comment'),
    
]