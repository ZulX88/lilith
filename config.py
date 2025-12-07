import os
from dotenv import load_dotenv, find_dotenv

env_path = find_dotenv()
load_dotenv(env_path)

apikeys={
  "nauval":os.getenv("NAUVAL_APIKEY", "")
}
public : bool = False
prefix = os.getenv("PREFIXES", "!").split(",")
namedb = os.getenv("NAMEDB", "db.sqlite3")
owner = os.getenv("OWNER", "").split(",")
bot_name = os.getenv("BOT_NAME", "Shiro Bot")
git_tok= os.getenv("GITHUB_TOKEN","")