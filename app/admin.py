from django.contrib import admin

# Register your models here.
from .models import Tip, User, UserTipped, Sport, TippingStrategy, BettingAccount, JoinUs
from django.contrib.auth.admin import UserAdmin

admin.site.register(User, UserAdmin)
admin.site.register(Sport)
admin.site.register(TippingStrategy)
admin.site.register(Tip)
admin.site.register(UserTipped)
admin.site.register(BettingAccount)
admin.site.register(JoinUs)
