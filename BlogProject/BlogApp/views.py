from django.shortcuts import render
from django.contrib.auth.models import User
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta
from django.http import JsonResponse
from .models import *

# Create your views here.

def render_page(request,author_id):
    print("this name function",author_id)
    name = author_id
    context = {"author_id":int(name)}
    return render(request,"BlogApp/blog.html",context)

def render_top_blog(request,author_id):
    author_id = author_id
    print("this name function", author_id)
    context = {'author_id' :author_id}
    return render(request,"BlogApp/top_blogs.html",context)


def render_top_liked_blogs(request):
    requested_user = request.user
    print("this name function", requested_user)
    context = {'requested_user' :requested_user}
    return render(request,"BlogApp/top_liked_blogs.html",context)


def render_blogs_comment(request):
    user_id = request.user
    print("this name function", user_id)
    context = {'user' :user_id}
    return render(request,"BlogApp/comment_history.html",context)


def render_author_comment(request, author_id):
    author_id = author_id
    print("this name function", author_id)
    context = {'author_id' :author_id}
    return render(request,"BlogApp/comment_history.html",context)


# def blog_data(request, author_id):
#     print("this is ",author_id)
#     user = User.objects.get(pk=int(author_id))
#     print("this is ",user)
#     blogs = Blog.objects.filter(author=user)
#     for blog in blogs:

#         comments_count = Comment.objects.filter(blog=blog).count()
#         likes_count = Response.objects.filter(blog=blog, like_or_not=True).count()
#         dislikes_count = Response.objects.filter(blog=blog, like_or_not=False).count()

    
#     commented_blogs = Blog.objects.filter(author_id=user).annotate(comment_count=Count('comment')).order_by('-comment_count')[:5]
    
#     three_days_ago = timezone.now() - timedelta(days=3)
    
#     liked_blogs = Blog.objects.filter(response__like_or_not=True, response__response_date__gte=three_days_ago).annotate(like_count=Count('response')).order_by('-like_count')[:5]
    
#     dislike_blogs = Blog.objects.filter(response__like_or_not=False, response__response_date__gte=three_days_ago).annotate(like_count=Count('response')).order_by('-like_count')[:5]
    
#     context = {"comments":list(commented_blogs.values()),"liked":list(liked_blogs.values()),"diliked":list(dislike_blogs.values())}

#     return JsonResponse({"comments":list(commented_blogs.values()),"liked":list(liked_blogs.values()),"diliked":list(dislike_blogs.values())})


def specific_author_data(request, author_id):
    blogs = Blog.objects.filter(author=User.objects.get(pk=author_id))
    data = []
    for blog in blogs:

        comments_count = Comment.objects.filter(blog=blog).count()
        likes_count = Response.objects.filter(blog=blog, like_or_not=True).count()
        dislike_count = Response.objects.filter(blog=blog, like_or_not=False).count()

        data.append({
            'blog_name':blog.name,
            'total_comments' :comments_count,
            'total_likes' :likes_count,
            'total_dislike' : dislike_count
        })
    
    return JsonResponse({'blogs': data})


def top_blog_data(request, author_id):
    user = User.objects.get(pk=int(author_id))
    three_days_ago = timezone.now() - timedelta(days=3)
    data = []

    commented_blogs = Blog.objects.filter(author_id=user).annotate(comment_count=Count('comment')).order_by('-comment_count')[:5]
    liked_blogs = Blog.objects.filter(response__like_or_not=True, response__response_date__gte=three_days_ago).annotate(like_count=Count('response')).order_by('-like_count')[:5]
    dislike_blogs = Blog.objects.filter(response__like_or_not=False, response__response_date__gte=three_days_ago).annotate(like_count=Count('response')).order_by('-like_count')[:5]
    
    for blog, like, dislike in zip(commented_blogs, liked_blogs, dislike_blogs):
        data.append({
            'top_blogs': blog.name,
            'comments_count': blog.comment_count,
            'liked_blogs' : like.name,
            'like_counts' : like.like_count,
            'disliked_blogs' : dislike.name,
            'dislike_counts' : dislike.like_count,

        })
    return JsonResponse({'top_commented_blogs': data})


def blog_reader_data(request):
    logged_user = request.user
    like_data = []
    liked_res = Response.objects.filter(user=logged_user, like_or_not=True).order_by('-response_date')[:5]
    for res in liked_res:
        like_data.append({
            'name' : res.blog.name,
        })

    return JsonResponse({'liked_blogs': like_data})


def comment_history(request):
    logged_user = request.user
    comm_history = []
    comments = Comment.objects.filter(user=logged_user).order_by('-created_date')
    for comm in comments:
        comm_history.append({
            'blogs' : comm.blog.name,
            'comments' : comm.comment_text
        })
    return JsonResponse({'history': comm_history})


def comment_history_author(request, author_id):
    logged_user = request.user
    comm_author = []
    comments = Comment.objects.filter(user=logged_user, blog__author_id=author_id).order_by('-created_date')
    for comm in comments:
        comm_author.append({
            'author' : comm.blog.author.username,
            'comments' : comm.comment_text
        })
    return JsonResponse({'author_comm': comm_author})
