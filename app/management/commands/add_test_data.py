from django.core.management.base import BaseCommand
from django.utils import timezone
import pandas as pd
from app.models import Tip


class Command(BaseCommand):
    help = "reads a csv into models"

    def handle(self, *args, **kwargs):
    	df = pd.read_csv("tips_csv.csv")
    	df["time"] = pd.to_datetime(df["time"], format="%d/%m/%Y")

    	for time, odds, sport, event, market in zip(df.time, df.odds, df.sport, df.event, df.market):
    		model = Tip(time=time, odds=odds, sport=sport, event=event, market=market)
    		model.save()