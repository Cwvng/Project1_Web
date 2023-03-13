from django.db import models
from django.contrib.auth import get_user_model
import uuid, random
from datetime import datetime

# Create your models here.

User = get_user_model()


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_user = models.IntegerField()
    bio = models.TextField(default='')
    name = models.TextField(default='')
    phone_number = models.TextField(default='')
    address = models.TextField(default='')
    email = models.TextField(default='')
    profileimg = models.ImageField(
        upload_to='profile_image', default='blank-profile-picture.png')

    def __str__(self):
        return self.user.username


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.TextField(max_length=100)
    image = models.ImageField(upload_to='post_images',
                              default='default_post_image.avif')
    createTime = models.DateTimeField(default=datetime.now)

    type = models.TextField(default='Cho thuê')
    housetype = models.TextField(default='Không chung chủ')

    # location
    location = models.TextField()
    district = models.TextField(default='Undefined District')
    # service price
    price = models.IntegerField(default=0)
    area= models.IntegerField(default=0)
    details = models.TextField()

    like_check= models.IntegerField(default=random.randint(1,99))

    user_wishList= models.ManyToManyField(User, related_name='user_wishList', blank=True)

    def __str__(self):
        return self.location
        
# class Wishlist (models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="wish_list")

# class WishlistItems(models.Model):
#     item =models.ForeignKey(Wishlist, on_delete=models.CASCADE, related_name="wishlist_items")
#     post= models.ForeignKey(Post, on_delete=models.SET_NULL, null= True, blank=True)

class LikePost(models.Model):
    post_id= models.CharField(max_length=500)
    username= models.CharField(max_length=100)

    def __str__(self):
        return self.post_id