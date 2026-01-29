from neonize.client import NewClient
import bot.config as config
from neonize.utils.enum import ClientName ,ClientType
client = NewClient(config.namedb)

number = input("Nomor WA : ")
client.PairPhone(str(number), show_push_notification=True)
