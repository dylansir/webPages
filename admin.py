from django.contrib import admin

from .models import User,  Bids, Listings, Comments, watchList


  
admin.site.register(Bids)
admin.site.register(Comments)
admin.site.register(User)
admin.site.register(Listings)
admin.site.register(watchList)
# Register your models here.
