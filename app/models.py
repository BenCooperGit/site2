from django.db import models

from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator

# Create your models here.
class User(AbstractUser):
	tips = models.ManyToManyField("Tip", through="UserTipped")
	first_name = models.CharField(max_length=30)
	last_name = models.CharField(max_length=30)
	email = models.EmailField(unique=True)

	#USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = [first_name, last_name, email]

	
	
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
