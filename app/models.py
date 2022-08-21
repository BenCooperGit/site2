from django.db import models

from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser, PermissionsMixin, BaseUserManager
from django.core.validators import MinValueValidator

# Create your models here.
class CustomAccountManager(BaseUserManager):

	def create_user(self, email, user_name, first_name, last_name, password, **other_fields):
		if not email:
			raise ValueError(_("You must provide an email address"))
		email = self.normalize_email(email)
		user = self.model(email=email, user_name=user_name, first_name=first_name, 
			last_name=last_name, **other_fields)
		user.set_password(password)
		user.save()
		return user

	def create_superuser(self, email, user_name, first_name, last_name, password, **other_fields):
		other_fields.setdefault("is_staff", True)
		other_fields.setdefault("is_superuser", True)
		other_fields.setdefault("is_active", True)

		if other_fields.get("is_staff") is not True:
			raise ValueError("superuser must be assigned to is_staff=True")

		if other_fields.get("is_superuser") is not True:
			raise ValueError("superuser must be assigned to is_superuser=True")

		return self.create_user(email, user_name, first_name, last_name, password, **other_fields)

class User(AbstractUser, PermissionsMixin):
	email = models.EmailField(_("email address"), unique=True)
	#username = models.CharField(max_length=30, unique=True)
	first_name = models.CharField(max_length=30, null=False)
	last_name = models.CharField(max_length=30, null=False)
	start_date = models.DateTimeField(default=timezone.now)
	is_staff = models.BooleanField(default=False)
	is_superuser = models.BooleanField(default=False)

	tips = models.ManyToManyField("Tip", through="UserTipped")

	objects = CustomAccountManager()

	USERNAME_FIELD = "email"
	REQUIRED_FIELDS = [email, first_name, last_name]
	
class Sport(models.Model):
	name = models.CharField(max_length=60)

class TippingStrategy(models.Model):
	name = models.CharField(max_length=60)
	sport = models.ForeignKey("Sport", null=True, on_delete=models.SET_NULL)

class Tip(models.Model):
	tip_source = models.ForeignKey("TippingStrategy", null=True, on_delete=models.SET_NULL)
	time = models.DateTimeField()
	match_clock = models.CharField(max_length=10, null=True)
	league = models.CharField(max_length=60, null=True)
	playera = models.CharField(max_length=60, null=True)
	playerb = models.CharField(max_length=60, null=True)
	market = models.CharField(max_length=60, null=True)
	selection = models.CharField(max_length=60, null=True)
	odds = models.FloatField(null=True)
	users = models.ManyToManyField("User", through="UserTipped")

	@classmethod
	def fields(self):
		return [field.name for field in self._meta.fields]

class UserTipped(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
	tip = models.ForeignKey(Tip, on_delete=models.CASCADE, null=True, blank=True)
	stake_suggested = models.FloatField()
	stake_bet = models.FloatField(default=0, validators=[MinValueValidator(0.0)])
	odds_bet = models.FloatField(null=True, validators=[MinValueValidator(1.0)])
	last_modified = models.DateTimeField(auto_now=True)
	user_entered_detail = models.BooleanField(default=False, null=False, blank=False)

class BettingAccount(models.Model):
	name = models.CharField(max_length=30)

class JoinUs(models.Model):
	first_name = models.CharField(max_length=30)
	last_name = models.CharField(max_length=30)
	email = models.EmailField()
	betting_accounts = models.ManyToManyField("BettingAccount")
	why_want_to_join = models.CharField(max_length=800)
