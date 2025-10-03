from neonize.client import NewClient
import config
client = NewClient(config.namedb)

number = input("Nomor WA : ")
client.PairPhone(str(number), show_push_notification=True)
