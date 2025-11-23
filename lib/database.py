import glob
import json
import os

JSON_DIR = "database"

all_db = {}

for filename in glob.glob(os.path.join(JSON_DIR, "*.json")):
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
            
        db_key = os.path.basename(filename).split(".json")[0]
        all_db[db_key] = data
        print(f"Successfully loaded : {db_key}✅")
   
    except Exception as err:
        print(err)
       
user_ban = all_db["user_ban"]
group_ban = all_db["group_ban"]
own_bot = all_db["alt_owner"]