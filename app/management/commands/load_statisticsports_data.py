from django.core.management.base import BaseCommand
from django.utils import timezone
import requests
import datetime as dt
import time
import sys
sys.path.append(r"C:\Users\benja\Documents\CURRENT\Unchained\site2\app\management\commands")
sys.path.append(r"C:\Users\benja\Documents\CURRENT\Unchained\site2")
from statisticsports_scanner import handle_notification
from app.models import Tip, TippingStrategy, User, UserTipped

def tip_user(tip):
	user = User.objects.all().first()
	user_tip_info = UserTipped(
		user=user,
		tip=tip,
		stake_suggested=30
		)
	user_tip_info.save()

def use_notification(notification):
	match_time, league, notification_name, home_team, away_team, selection, odds, market = handle_notification(notification)
	print(f"\nLeague: {league}\nNotification name: {notification_name}\nHome team: {home_team}\nAway team: {away_team}")
	print(f"Market: {market}\nSelection: {selection}\nOdds: {odds}\n")
	tip = Tip(
		tip_source=TippingStrategy.objects.filter(name__exact="ss-"+notification_name).first(),
		time_utc=dt.datetime.now(),
		match_clock=match_time,
		league=league,
		playera=home_team,
		playerb=away_team,
		market=market,
		selection=selection,
		odds=odds
		)
	tip.save()
	tip_user(tip)
	#https://www.revsys.com/tidbits/tips-using-djangos-manytomanyfield/

class Command(BaseCommand):
	help = "Receives notifications from statistic sports and inserts them into django models."

	def handle(self, *args, **kwargs):
		base_url = "https://statisticsports.com/en/live-games?request_latest_notifications=1&_="
		i = 1659640994900
		cookie = '_hjSessionUser_2248152=eyJpZCI6IjM1NGE2ODNiLTcxNTEtNTE5MC04NDlkLTIwMjQ3YTAwZjRiYyIsImNyZWF0ZWQiOjE2NTE1MDQ1NTY2NTcsImV4aXN0aW5nIjp0cnVlfQ==; gdpr-law-consent=1; _fbp=fb.1.1655663452146.1318535214; _gcl_au=1.1.85408566.1659280949; _gid=GA1.2.768264556.1659551064; remember_web_59ba36addc2b2f9401580f014c7f58ea4e30989d=eyJpdiI6IitSdUZFTTA5OUdTVTUzWmlnVG81NFE9PSIsInZhbHVlIjoidGVPK1NVWGk5WU42akcrRk9WQ09ycWZIbU9VakJudGFmdlRydHpCbnNoeDM4c2oxY3ZGc1hsSkE0bDNQMGZ2QVpkVGZMTnh2QmNObnhNdThZRHFxTXE0TVpJVUNjYXpUSDFzRjZjQi9FRVpSMkhUTDVnSDY5TmdLTEcvY2tidmxGdnZIRWhHYTJlV2JkZ0Z5cHJNZ3ZDQTVjSFZJUjVTTXY1OVVTczNyL2M3ZVNyQm5IcVJYdXBYUG5zeC82a280QlNKQ1Y4YXYydTV1alhlU1JYUE5ETnJFK0N6M3NwQ0RjZ3hDWHdpcjhRaz0iLCJtYWMiOiI4ZDQyODgyOWQ2ZWRkMTJhYTAyZGViZmEzNjUxOGI5MTAyNTFjOTYwOGFjYWJhYTBiYjgxYjRhN2Q2ODNjYWFjIn0=; statisticsports_session=c221Ayss6F9RwTzrm8POjYaEI49GF6qkMbY8h3P4; _hjSession_2248152=eyJpZCI6ImZlY2Q1ZGE2LTY0ODYtNDQ2Ni1iY2FjLTc0ZTg1NzYzZGJmNiIsImNyZWF0ZWQiOjE2NTk2NDA5MTc5NDEsImluU2FtcGxlIjpmYWxzZX0=; pfd=d534f14f7bd9440f719e212a720aa421; _gat=1; _gat_UA-96060949-1=1; __cf_bm=Ocprc_lCeJzNtb7OOY9_GlQIDlpRHtJIEp0vnyp4DH4-1659640993-0-AU4BCBdhiH/DBYDdxYhtuvlilal7jxkYKeKYr0RZW6e0zIbRmHTCAFJIc/gUtdmLME+evEUuJV7rvfnbAYnYZW6jqLQUrbdyymkfh6YsxIZuaNZbkmeORZ0v7JVmLrIHSg==; utmdata=eyJpdiI6ImpaYnYzQUEwMGJLREp5SE9aSTlGYXc9PSIsInZhbHVlIjoicmFtVGpRTVdYcks0ekNLc05RZENManJ5MVVTem9HNDVoN3daYzVnTjJDTTAvWUYvS2hZVGgramdhZG4ySFlyc3krOUh4b0dEaGd1ak9nd0NjL1RTUElKaEI1eTBDR1Jsa1UwNFB2UTk4SzBDalJHSFBpUEZPZHplSWt5TEM2enUiLCJtYWMiOiJhZDQ2NGY2ZWY5OWE1NjE5YWVjZDA0ZTAyMWRkMDdmNTU5M2ZjNzdhYTZlYjA0NjNhMDM1ZWE3M2QxMWNmZjYzIn0=; _ga_HKFHWM0RJ1=GS1.1.1659640911.50.1.1659640995.51; _ga=GA1.2.1913488509.1651504541; XSRF-TOKEN=eyJpdiI6IkNYazl6SkhSNjRtL0RUaGFUbXlGWWc9PSIsInZhbHVlIjoia3dhcWJNSDg5bE9WSzE2aDM1Z3NzSk03WUpjZDY0T1JJRjRwUkNHdFNLRXloZ0VyRWZxVnM4am5PQWZvUWZjUUM3eUd2anNkZlR5NjRVKzZqeXFXdmpDQUhDNzBORWFRdXFmbFk5NUFUOEVuRFlGY1paSmEvc1VKenZxdXByUlAiLCJtYWMiOiIzNTk2NDI5NzUxMzVjMDk2ZDU1ZGYyODcxM2YwMTE1Mzk2OTFmYjBlOWY1NWY4ZTY4NGEyM2JjMWI0ZDE4NTVlIn0'
		headers = {
					'authority': 'statisticsports.com',
					'accept': 'application/json, text/javascript, */*; q=0.01',
					'accept-language': 'en-US,en;q=0.9',
					'cookie': cookie,
					'dnt': '1',
					'referer': 'https://statisticsports.com/en/live-games',
					'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
					'sec-ch-ua-mobile': '?0',
					'sec-ch-ua-platform': '"Windows"',
					'sec-fetch-dest': 'empty',
					'sec-fetch-mode': 'cors',
					'sec-fetch-site': 'same-origin',
					'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
					'x-requested-with': 'XMLHttpRequest'
					}


		seen_notifications = dict()
		# Add first notifications seen to list
		response = requests.request("GET", base_url + str(i), headers=headers)
		response_json = response.json()
		notifications_list = response_json["latest_notifications"]
		for notification in notifications_list:
			notification_id = notification["id"]
			seen_notifications[notification_id] = dt.datetime.now()
		while True:
			i = i + 1
			url = base_url + str(i)
			response = requests.request("GET", url, headers=headers)
			response_json = response.json()
			#print(response.text)
			notifications_list = response_json["latest_notifications"]
			if notifications_list:  # Not empty
				for notification in notifications_list:
					notification_id = notification["id"]
					datetime_now = dt.datetime.now()
					if (notification_id not in seen_notifications):
						seen_notifications[notification_id] = datetime_now
						use_notification(notification)
					elif (datetime_now - seen_notifications[notification_id]) > dt.timedelta(minutes=5):
						seen_notifications.pop(notification_id)
						# handle notification
						use_notification(notification)
			time.sleep(1)

# python manage.py load_statisticsports_data