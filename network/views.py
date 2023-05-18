from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json
from django.core.paginator import Paginator
from .models import *


def index(request):
    all_posts = newPost.objects.all().order_by('-date')
    user_likes = likePost.objects.filter(user=request.user.id).values_list("post", flat=True)
    likes = likePost.objects.all().values_list("post", flat=True)
    num_likes = {}
    for j in likes:
        if j in num_likes:
            num_likes[j] +=1
        else:
            num_likes[j] =1

    contact_list = newPost.objects.all().order_by('-date')
    paginator = Paginator(contact_list, 10) # Show 10 contacts per page.

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    print(page_obj)
    return render(request, "network/index.html",{
        "posts": all_posts,
        "likes": user_likes,
        "num_likes": num_likes,
        "message": "All Posts",
        "page_obj": page_obj,
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
    user_likes = likePost.objects.filter(user=request.user.id).values_list("post", flat=True)
    likes = likePost.objects.all().values_list("post", flat=True)
    user = User.objects.get(id=id)
    num_likes = {}
    for j in likes:
        if j in num_likes:
            num_likes[j] +=1
        else:
            num_likes[j] =1

    return render(request, "network/profile.html",{
        "page_obj": all_posts,
        "following": following.count(),
        "followers" : followers.count(),
        "myfollowers": followers,
        "id": id,
        "username": username.username,
        "likes": user_likes,
        "num_likes": num_likes,
        "user": user,
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
               
    user_likes = likePost.objects.filter(user=request.user.id).values_list("post", flat=True)
    likes = likePost.objects.all().values_list("post", flat=True)
    num_likes = {}
    for j in likes:
        if j in num_likes:
            num_likes[j] +=1
        else:
            num_likes[j] =1

    return render(request, "network/index.html",{
        "page_obj": following_post,
        "likes": user_likes,
        "num_likes": num_likes,
        "message": "Following Posts",
    })

@csrf_exempt
@login_required
def postLikes(request, id):
    if request.method == "GET":

        post = likePost.objects.get(post=id, user=request.user)
        return JsonResponse(post.serialize())

    elif request.method == "POST":

        post = newPost.objects.get(id=id)
        data = json.loads(request.body)

        post_like = newPost.objects.get(id=data["post"])

        try:
            test_like = likePost.objects.get(user=request.user, post=post_like, like=data["like"])
        except likePost.DoesNotExist:
            likePost.objects.create(user=request.user, post=post_like, like=data["like"])
            print(data)

        if test_like:
            likePost.objects.get(user=request.user, post=post_like, like=data["like"]).delete()

        return HttpResponse(status=204)
    
@csrf_exempt
@login_required
def editPost(request, id):
    try:
        post = newPost.objects.get(id=id)
            
    except newPost.DoesNotExist:
        return JsonResponse({"error": "Not found."}, status=404)
        
    if request.method == "GET":
        return JsonResponse(post.serialize())

    elif request.method == "PUT":

        data = json.loads(request.body)
        print(data["id"], data["text"])
        try:
            edited_post = newPost.objects.get(id=data["id"])

        except newPost.DoesNotExist:
            return JsonResponse({"error": "Not found."}, status=404)

        if edited_post.text != data["text"]:
            newPost.objects.filter(id=data["id"]).update(text=data["text"])
            print("succsses")

    return HttpResponse(status=204)
