from django.contrib import admin

# Register your models here.
from .models import Tip, User, UserTipped, Sport, TippingStrategy, BettingAccount, JoinUs
from django.contrib.auth.admin import UserAdmin

class UserAdminConfig(UserAdmin):
	search_fields = ("email", "first_name")
	#list_filter = ("is_active", "is_staff")
	ordering = ("-start_date",)
	list_display = ("email", "first_name", "is_active", "is_staff")

	# fieldsets = (
	# 	(None, {"fields": ("email", "first_name")}),
	# 	("permissions", {"fields": ("is_staff", "is_active")}),
	# 	("personal", {"fields": ("last_name",)}),
	# )

	add_fieldsets = (
		(None, {
			"classes": ("wide",),
			"fields": ("email", "first_name", "last_name", "password1", "password2"),
			}
		),
	)

admin.site.register(User, UserAdminConfig)
admin.site.register(Sport)
admin.site.register(TippingStrategy)
admin.site.register(Tip)
admin.site.register(UserTipped)
admin.site.register(BettingAccount)
admin.site.register(JoinUs)
