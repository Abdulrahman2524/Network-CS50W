from datetime import datetime
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json
from .models import *


def index(request):
    all_posts = newPost.objects.all().order_by('-date')
    return render(request, "network/index.html",{
        "posts": all_posts,
        "message": "All Posts",
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
    
@login_required
def sharePost(request):
    if request.method == "POST":
        user = request.user
        post = request.POST["post"]

        if post is not None:
            newPost.objects.create(user=user, text=post)
            return HttpResponseRedirect(reverse("index"))
        else:
            return HttpResponseRedirect(reverse("index"))

    else:
        return HttpResponseRedirect(reverse("index"))
    
@login_required
def profile(request, id):
    all_posts = newPost.objects.filter(user=id).order_by('-date')
    following = UserFollowing.objects.filter(user_id=id)
    followers = UserFollowing.objects.filter(following_user_id = id)
    username = User.objects.get(id=id)
    return render(request, "network/profile.html",{
        "posts": all_posts,
        "following": following.count(),
        "followers" : followers.count(),
        "id": id,
        "username": username.username
    })

@csrf_exempt
@login_required
def show_follower(request, id):

    try:
        user = UserFollowing.objects.get(user_id=request.user.id, following_user_id=id)
        
    except UserFollowing.DoesNotExist:
        return JsonResponse({"error": "Not found."}, status=404)
    
    if request.method == "GET":
        return JsonResponse(user.serialize())
    
    
@csrf_exempt
@login_required
def follow(request, id):

    if request.method == "POST":
        data = json.loads(request.body)
        following_list = UserFollowing.objects.filter(user_id=request.user, following_user_id=data['following_user_id']).count()
        follower = User.objects.get(pk=data['following_user_id'])
        if following_list == 0:
            UserFollowing.objects.create(user_id=request.user, following_user_id=follower)
            print(following_list)
        else:
            print("in It")

        return HttpResponse(status=204)

@csrf_exempt
@login_required
def unFollow(request, id):
        
    if request.method == "POST":
        data = json.loads(request.body)
        UserFollowing.objects.get(user_id=request.user, following_user_id=data['following_user_id']).delete()

        return HttpResponse(status=204)

@login_required
def followingPosts(request):

    user = UserFollowing.objects.filter(user_id=request.user).values_list("following_user_id", flat=True)
    following_post = []
    for i in range(len(user)):

        new = newPost.objects.filter(user=user[i]).order_by('-date')
        for i in new:

            following_post.append(i)
               
    
    return render(request, "network/index.html",{
        "posts": following_post,
        "message": "Following Posts",
    })
