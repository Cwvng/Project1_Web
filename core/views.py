from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from .models import Profile, Post, LikePost

from django.db.models import Q

# Create your views here.

# Trang chủ


@login_required(login_url='signin')
def index(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)

    # sort
    if request.GET.get('sortBy') != None and request.GET.get('q') == None:
        p = Paginator(Post.objects.all().order_by(
            request.GET.get('sortBy')), 3)
    elif request.GET.get('sortBy') == None and request.GET.get('q') != None:
        q = request.GET.get('q')
        multiple_q = Q(Q(district__icontains=q) | Q(
            details__icontains=q) | Q(type__icontains=q) | Q(location__icontains=q) | Q(housetype__icontains=q))
        p = Paginator(Post.objects.filter(multiple_q), 3)
    else:
        p = Paginator(Post.objects.all().order_by('-createTime'), 3)

    page = request.GET.get('page')
    postPage = p.get_page(page)
    resultNumber = len(postPage)
    context = {'user_profile': user_profile,
               'postPage': postPage,
               'resultNumber': resultNumber}
    return render(request, 'index.html', context)


# Thao tác người dùng
def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        cfPassword = request.POST['cfpassword']
        if cfPassword == password:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username already used')
                return redirect('signup')
            else:
                user = User.objects.create_user(
                    username=username, password=password)
                user.save()

                # log user to settings account
                # user_login = auth.authenticate(
                #     username=username, password=password)
                # auth.login(request, user_login)

                # create a profile object for the new user
                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(
                    user=user_model, id_user=user_model.id)
                new_profile.save()
                return redirect('signin')
        else:
            messages.info(request, 'Password is not retyped correctly')
            return redirect('signup')
    else:
        return render(request, 'signup.html')


def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Username or password is incorrect')
            return redirect('signin')
    else:
        return render(request, 'signin.html')


def logout(request):
    auth.logout(request)
    return redirect('/')


# Tính năng web
@login_required(login_url='login')
def settings(request):
    user_profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':

        if request.FILES.get('image') == None:
            image = user_profile.profileimg
            name = request.POST['name']
            phone_number = request.POST['phone_number']
            address = request.POST['address']
            email = request.POST['email']

            user_profile.profileimg = image
            user_profile.name = name
            user_profile.phone_number = phone_number
            user_profile.address = address
            user_profile.email = email
            user_profile.save()

        if request.FILES.get('image') != None:
            image = request.FILES.get('image')
            name = request.POST['name']
            phone_number = request.POST['phone_number']
            address = request.POST['address']
            email = request.POST['email']

            user_profile.profileimg = image
            user_profile.name = name
            user_profile.phone_number = phone_number
            user_profile.address = address
            user_profile.email = email
            user_profile.save()

        return redirect('settings')

    return render(request, 'settings.html', {'user_profile': user_profile})


def upload(request):
    if request.method == 'POST':
        user = request.user.username
        image = request.FILES.get('image_upload')
        price = request.POST['price']
        location = request.POST['location']
        district = request.POST['district']
        details = request.POST['details']
        type = request.POST['type']
        area = request.POST['area']
        housetype = request.POST['housetype']

        new_post = Post.objects.create(
            user=user, image=image, price=price, location=location, details=details, type=type, district=district, housetype=housetype, area=area)
        new_post.save()
        messages.success(request, "uploaded your new post!!")
        return render(request, 'upload.html', {'new_post': new_post})

    return render(request, 'upload.html')


def inforpage(request, postid):

    user_post = Post.objects.get(id=postid)
    # user_profile=Profile.objects.get(user_post__id== postid, user = user_post__user)

    context = {
        'user_post': user_post,
        # 'user_profile':user_profile,
    }

    return render(request, 'inforpage.html', context)

# def addToWishList(request, id):
#     post = Post.objects.get(id= id)
#     user= request.user

#     item, _ = Wishlist.objects.get_or_create(user= user )

#     wishlist_items= WishlistItems.objects.create(post= post, item = item)
#     wishlist_items.save()
#     messages.success(request, "A new room had added to your Wishlist")

#     return redirect('/')


@login_required(login_url='login')
def like_post(request):
    username = request.user.username
    post_id = request.GET.get('post_id')

    post = Post.objects.get(id=post_id)

    like_filter = LikePost.objects.filter(
        post_id=post_id, username=username).first()

    if like_filter == None:
        new_like = LikePost.objects.create(post_id=post_id, username=username)
        new_like.save()
        post.like_check = post.like_check+1
        post.save()
        return redirect('/')
    else:
        like_filter.delete()
        post.like_check = post.like_check-1
        post.save()
        return redirect('/')


@login_required(login_url='login')
def add_to_wishList(request, postid):
    # item = Post.objects.get(id= postid)
    item = get_object_or_404(Post, id=postid)
    if item.user_wishList.filter(id=request.user.id).exists():
        item.user_wishList.remove(request.user)
        messages.success(request, "Removed from your Wishlist")
    else:
        item.user_wishList.add(request.user)
        messages.success(request, "Added a new room to your Wishlist")
    return HttpResponseRedirect(request.META["HTTP_REFERER"])

@login_required(login_url='login')
def wishList(request):
    item = Post.objects.filter(user_wishList= request.user)
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)
    total = len(item)
    return render(request, 'wishList.html', {'saved_post': item, 'user_profile': user_profile, 'count_post':total})