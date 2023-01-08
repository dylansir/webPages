from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from django.contrib import messages
import re
from django.core.exceptions import ObjectDoesNotExist

from .models import User, Listings, Create, Bids, Comments, watchList

CategoriesList = (
    ('Sports', 'Sports'),
    ('Leisure', 'Leisure'),   
    ('Video Games', 'Video Games'), 
    ('Kitchen' , 'Kitchen'),
    ('Electronics', 'Electronics'),
    ('Garden', 'Garden')
)

b = [
    'labelz',
    'boxez'
]

a = [
    'Title',
    'Description',
    'Categories',
    'Image',
    'startingBid'
]

class ListingForm(forms.Form):
    Title = forms.CharField(label="Title", 
            widget=forms.TextInput(attrs={'id': f'{b[0]}', 'title': f'{a[0]}', 'placeholder': 'Baseball bat..'}))
    Description = forms.CharField(label="Description", 
            widget=forms.Textarea(attrs={'id': f'{b[0]}', 'title': f'{a[1]}', 'max_length':'200', 'size':'20', 'placeholder': 'Write a description about your item'}))
    ##Figure out how to implement a list to drop down from. below
    Categories = forms.ChoiceField(choices=CategoriesList)
    ##Figure out how to allow an image input.
    Image = forms.CharField(label="Image", 
            widget=forms.URLInput(attrs={'id': f'{b[0]}', 'title': f'{a[3]}', 'size':'5', 'placeholder': 'Add a URL to display an image'}))
    startingBid = forms.IntegerField(label="Starting Bid", 
            widget=forms.TextInput(attrs={'id': f'{b[0]}', 'title': f'{a[4]}', 'size':'5', 'placeholder': '50'}))



listings = Listings()



def index(request):

    displayListing = Listings.objects.all()
    #prevBids = listings.Bids.bidHistory.count()


    if request.user.is_authenticated:
        
        return render(request, "auctions/index.html", {
                        "form":ListingForm,
                        "item":displayListing,
                        #"prevBids":prevBids
                    })
    else:
        return render(request, "auctions/login.html")


#     _____________________________________________________    #
def submitListing(request, ):

    
    if request.user.is_authenticated:

        bids = Bids()
        comments = Comments()

        if request.method == "POST":

            current_user = request.user

            if (Listings.objects.filter(Name=request.POST[f'{a[0]}'])):  

                daMessage = messages.error(request, "Listing name already in use, try something else")                    

            else:

                daMessage = messages.success(request, "Listing submitted succesfully.")


                count = Listings.objects.all().count() + 1


                 
                Name = request.POST[f'{a[0]}']

                
                bids.currentBid=request.POST[f'{a[4]}']                   
                bids.User=current_user
                bids.Name=Name
                bids.save() 

                comments.Comments="Null User"
                comments.User=current_user
                comments.save()
                
                listings.Name=Name
                listings.Description=request.POST[f'{a[1]}']
                listings.Categories=request.POST[f'{a[2]}']
                listings.Image=request.POST[f'{a[3]}']
                listings.User=current_user
                listings.Bids= Bids.objects.get(pk=count)
                listings.Comments=Comments.objects.get(pk=count)

                

                listings.save()


            return HttpResponseRedirect(reverse("index"), daMessage) 

    return render(request, "auctions/submitlisting.html",{
                                "form":ListingForm
        })  

def login_view(request):

    if request.method == "POST":


        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)


        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]


        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })


        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def watchlist(request):

    return render(request, "auctions/watchlist.html")

def bidPlace(request):



    if request.method=="POST":



        listingid = request.POST["listing_id"]
        bidId = request.POST["bid_id"]

        updateBid = int(request.POST["Bid"])

        current_user = request.user

        newBids = Bids.objects.get(pk=bidId)
               
        if updateBid <= newBids.currentBid:

            daMessage = messages.error(request, "Bid must be higher than the current bid")     
                    
            return render(request, "auctions/placebid.html", {
                    "item":Listings.objects.filter(pk=listingid),
                    "userMessage": daMessage
                })

        else:      
                newBids.User=current_user
                newBids.currentBid=updateBid

                newBids.save()

                Bids.objects.get(pk=bidId).add_bid()


                daMessage = messages.success(request, "You have succesfully placed a bid." )

                return HttpResponseRedirect(reverse("index"), daMessage)

        
    return render(request, "auctions/placebid.html", {
           # "wholeListing":Listings.objects.filter(Name=)
        })


def viewListing(request):

    #Listings_id = request.POST["name"]
    #listingName = Listings.objects.filter(id=Listings_id)

    if request.method=="POST":

        Listings_id = request.POST["name"]
        listingName = Listings.objects.filter(id=Listings_id)


    return render(request, "auctions/viewListings.html", {
            "wholeListing":listingName,
    })


def watchlist(request):

    if request.user.is_authenticated:


        try:
            
            ##I know i have made a lot of boilerplate code here, but I just watned to be safe for now :P

            current_user = request.user
            user_to_split=re.split("\s", str(request.user), 1)

            actual_user = user_to_split[0]
            
            user_id=User.objects.get(username=actual_user).id
            watchList_ = watchList.objects.filter(User=user_id)
            if request.method=="POST":

                    listing_id = request.POST["listing_id"]
                    watchlist_update = watchList()
                    watchlist_update.User=current_user
                    watchlist_update.Listing=Listings.objects.get(pk=listing_id)
                    watchlist_update.save()

            return render(request, "auctions/watchlist.html", {
                    "item":watchList_,
                    "user_display":actual_user
                })
        
        except(ObjectDoesNotExist):

            current_user=re.split("\s", str(request.user), 1)

            actual_user = current_user[0]

            return render(request, "auctions/watchlist.html", {
                    #"item":watchList_,
                    "user_display":actual_user,
                    "noListing":True
                })


    
    else:
        return HttpResponseRedirect(reverse("index"))
    