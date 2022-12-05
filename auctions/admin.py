from django.contrib import admin
from .models import auction_listing, bid, comment, watchlist, closed_listing

# Register your models here.

admin.site.register(auction_listing)
admin.site.register(bid)
admin.site.register(comment)
admin.site.register(watchlist)
admin.site.register(closed_listing)





