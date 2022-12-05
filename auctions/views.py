from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages

from .models import User, auction_listing, bid, comment, watchlist, closed_listing

def categories(request):
    if request.method == "POST":
        if request.POST.get("1"):
            code = request.POST.get("1")
        if request.POST.get("2"):
            code = request.POST.get("2")
        if request.POST.get("3"):
            code = request.POST.get("3")
        if request.POST.get("4"):
            code = request.POST.get("4")
        if request.POST.get("5"):
            code = request.POST.get("5")
        if request.POST.get("6"):
            code = request.POST.get("6")
        if request.POST.get("7"):
            code = request.POST.get("7")
        if request.POST.get("8"):
            code = request.POST.get("8")
        if request.POST.get("9"):
            code = request.POST.get("9")
        if request.POST.get("10"):
            code = request.POST.get("10")

        electronics_listings = auction_listing.objects.filter(category = code)

        return render(request, "auctions/categories_view.html", {
            "category": code,
            "listing": electronics_listings
        })
           

    return render(request, "auctions/categories.html")

def watchlist_items(request):
            
            #watchlist.objects.create(auction_id=request.POST.get("auction_id"), user=request.POST.get("user"))       

    watchlist_items = watchlist.objects.filter(user=request.user)

    auction_list=[]

    for item in watchlist_items:
        auction_item = auction_listing.objects.filter(id = item.auction_id)
        auction_list.append(auction_item[0])


    return render(request, "auctions/watchlist.html", {
        "watchlist": watchlist_items,
        "count": watchlist_items.count(),
        "auction_list": auction_list
    })

def listing_page(request, auction_id):
   
    bid_objects = bid.objects.filter(auction_id = auction_id)
    a = auction_listing.objects.filter(id=auction_id)
    watchlist_items = watchlist(user=request.user)
    w_items = watchlist.objects.filter(user=request.user)
    watchlist_items = watchlist.objects.filter(user=request.user)

    all_elements= { "auction_listing": a[0],
                "watchlist_items": watchlist_items,
                "auction_id": auction_id,
                "bid_count": bid_objects.count(),
                "current_user": str(request.user)
                }

    all_elements["count"] = watchlist_items.count() 

    if request.method == "POST":

        if request.POST.get("publish") == "Publish comment":
            comment_user = request.POST.get("user")
            message = request.POST.get("comment")

            new_comment = comment.objects.create(auction_id = auction_id, user = comment_user, message = message)
            new_comment.save()

            comments = reversed(comment.objects.filter(auction_id = auction_id))
            
            all_elements ["comments"] = comments

            return render(request, "auctions/listing_page.html", all_elements)

        elif request.POST.get("close_listing") == "Close auction":
            comments = reversed(comment.objects.filter(auction_id = auction_id))
            
            all_elements ["comments"] = comments

            bid_objects = bid.objects.filter(auction_id = auction_id)
            highest_price = [0]
            for bid_object in bid_objects:
                price = bid_object.bid_price
                highest_price.append(price)
            username = bid.objects.filter(bid_price = max(highest_price))         

            all_elements["congrats_message"]= "Congrats " + username[0].user + "! You won with a bid of $" + str(max(highest_price)) 
            all_elements["closed"] = "Yes"
            all_elements["listing_closed"] = "This listing is closed. This means that you cannot make another bid"
            
            auction_listing.objects.filter(id = auction_id).update(bid_closed="closed")

            return render(request, "auctions/listing_page.html", all_elements)
 
        elif request.POST.get("AddRemove") == "Remove from watchlist":
            watchlist_items = watchlist.objects.filter(user=request.user)
            all_elements["AddRemove"] = "Add to watchlist"
            watchlist.objects.filter(auction_id=auction_id).delete()
            all_elements["count"] = watchlist_items.count()
            return render(request, "auctions/listing_page.html", all_elements)
        elif request.POST.get("AddRemove") == "Add to watchlist":
            watchlist_items = watchlist.objects.filter(user=request.user)
            all_elements["AddRemove"] = "Remove from watchlist"
            user = str(request.user)
            newlist = watchlist.objects.create(auction_id = auction_id, user = user)
            watchlist.save(newlist)
            all_elements["count"] = watchlist_items.count()
            return render(request, "auctions/listing_page.html", all_elements)
        else:
            comments = reversed(comment.objects.filter(auction_id = auction_id))
            
            all_elements ["comments"] = comments
            try: 
                entry_bid = float(request.POST.get("bid"))
            except: 
                
                all_elements["error_message"] = "You need to input a real number"
                all_elements["AddRemove"] = request.POST.get("AddRemoveBid")
                return render(request, "auctions/listing_page.html", all_elements)
            
            bid_objects = bid.objects.filter(auction_id = auction_id)
            
            highest_price = [0]
            for bid_object in bid_objects:
                price = bid_object.bid_price
                highest_price.append(float(price))
            
            if entry_bid <= float(a[0].starting_bid) or entry_bid <= max(highest_price):
                all_elements["error_message"] = "Your bid is too low!"
                
                #This makes sure that the addremove input tag stays the same on refresh

                all_elements["AddRemove"] = request.POST.get("AddRemoveBid")
                return render(request, "auctions/listing_page.html", all_elements)
            
            else: 
                b = bid(auction_id=auction_id, user=request.user, bid_price=entry_bid)
                b.save()
                all_elements["success_message"] = "Your bid has been approved"

                bid_objects = bid.objects.filter(auction_id = auction_id)

                #This makes sure that the addremove input tag stays the same on refresh

                all_elements["AddRemove"] = request.POST.get("AddRemoveBid")
                all_elements["bid_count"] = bid_objects.count()

                print(bid_objects)
                print(bid_objects.count())
                return render(request, "auctions/listing_page.html", all_elements)

    if request.method == "GET":
        comments = reversed(comment.objects.filter(auction_id = auction_id))
            
        all_elements ["comments"] = comments

        auction_list = auction_listing.objects.filter(id = auction_id)
        if auction_list[0].bid_closed == "closed":
            bid_objects = bid.objects.filter(auction_id = auction_id)
            highest_price = [0]
            for bid_object in bid_objects:
                price = bid_object.bid_price
                highest_price.append(price)
            username = bid.objects.filter(bid_price = max(highest_price))  

            if str(request.user) == str(username[0].user):
                all_elements["congrats_message"] = "Congratulations! You won the auction with a bid of $" + str(max(highest_price))
            else: 
                all_elements["congrats_message"] = "Congrats " + username[0].user + "! You won with a bid of $" + str(max(highest_price)) 

        
            all_elements["closed"] = "Yes"
            all_elements["listing_closed"] = "This listing is closed. This means that you cannot make another bid"

            return render(request, "auctions/listing_page.html", all_elements)

        
        for w_item in w_items:
            if w_item.auction_id == auction_id:
                all_elements["AddRemove"] = "Remove from watchlist"
                return render(request, "auctions/listing_page.html", all_elements)
                
        all_elements["AddRemove"] = "Add to watchlist"
        return render(request, "auctions/listing_page.html", all_elements)

def create_list(request):
    watchlist_items = watchlist.objects.filter(user=request.user)

    if request.method == "POST":
        user = request.user
        title = request.POST.get("title")
        description = request.POST.get("description")
        starting_bid = request.POST.get("starting_bid")
        url = request.POST.get("url")
        category = request.POST.get("category")

        #You left off right here trying to access the database !
        
        a = auction_listing(user = user, title=title, description=description, starting_bid=starting_bid, url=url, category=category)
        a.save()

        return HttpResponseRedirect(reverse("index"))

        #return render(request, "auctions/index.html")

    return render(request, "auctions/create_list.html", {
         "count": watchlist_items.count()
    })

def index(request):
    auctions = auction_listing.objects.all()
    watchlist_items = watchlist.objects.filter(user=request.user)

    return render(request, "auctions/index.html", {
        "auctions": auctions,
        "count": watchlist_items.count()
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

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
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
