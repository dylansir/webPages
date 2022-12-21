from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib import admin
from django.conf import settings




class User(AbstractUser):
    pass
    WATCHLIST=[]
    watchList = models.CharField(WATCHLIST, default="None", max_length=100)
    def __str__(self):
        return '%s %s' % (self.username, self.last_login)

class Bids(models.Model):
    #BIDHISTORY = {}
    User = models.ForeignKey(User, default=0, on_delete=models.CASCADE)
    Name = models.CharField(max_length=64, default="Null")
    currentBid = models.PositiveIntegerField(default=0, blank=True)
    bidHistory = models.PositiveIntegerField(default=0)

  
    
    def __int__(self):
        return f"{self.currentBid}, {self.bidHistory}"
    
    def __str__(self):
        return f"{self.id}, {self.currentBid}, {self.bidHistory}"


    def add_bid(self):
        self.bidHistory += 1
        self.save()

class Comments(models.Model):
    User = models.ForeignKey(settings.AUTH_USER_MODEL, default=0, on_delete=models.CASCADE)
    Comments = models.CharField(max_length=250, default="Null")



    def __str__(self):
        return f"{self.User}, {self.Comments}, {self.id}"



class Listings(models.Model):

    CATEGORIES = [
    ('Sport', 'Sport'),
    ('Garden', 'Garden'),
    ('Kitchen', 'Kitchen'),
    ('Leisure', 'Leisure'),
    ('Electronics', 'Electronics'),
    ('VideoGames', 'VideoGames')
    ]

    User = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=models.CASCADE)
    Name = models.CharField(max_length=64)
    Description = models.CharField(max_length=64)
    Image = models.URLField(max_length=100, default='No_Image')
    Categories = models.CharField(CATEGORIES, max_length=25)
    Comments = models.ForeignKey(Comments, default=0, related_name="Listing", on_delete=models.CASCADE)
    Bids = models.ForeignKey(Bids, default=0, related_name="Listing", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.Name}, {self.Description}, {self.Image}, {self.Categories}"


class watchList(models.Model):

    User = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=models.CASCADE)
    Listing = models.ForeignKey(Listings, default=0, related_name="watchList", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.User}, {self.Listing}"



class Create(models.Manager):
    def create(self, user):
        created = self.create(User=user)
            # do something with the creation
        return created
