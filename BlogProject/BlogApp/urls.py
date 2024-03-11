from django.urls import path
from . import views

urlpatterns = [
    path("index/<str:author_id>/",views.render_page, name="index"),
    # path('<int:author_id>/', views.blog_data, name='home'),
    path('<int:author_id>/', views.specific_author_data, name='specific_author_data'),
    path("top_blog/<str:author_id>/",views.render_top_blog, name="top_blog"),
    path("top_liked_blogs/",views.render_top_liked_blogs, name="top_liked_blogs"),
    path("commented_blogs/",views.render_blogs_comment, name="commented_blogs"),
    path("commented_authors/<int:author_id>/",views.render_author_comment, name="commented_authors"),
    path('top_blog_data/<int:author_id>/', views.top_blog_data, name='top_blog_data'),
    path('blog_reader_data/', views.blog_reader_data, name='blog_reader_data'),
    path('comment_history/', views.comment_history, name='comment_history'),
    path('comment_history_author/<int:author_id>/', views.comment_history_author, name='comment_history_author')
]

