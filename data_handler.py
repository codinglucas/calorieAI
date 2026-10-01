import json
from datetime import datetime

def update_daily_records():
    filename = "record.json"
    dt_now = str(datetime.now().date())
    print(dt_now)

    with open(filename, "r") as file:
        data = json.load(file)
                    
    data[dt_now] = ""

    with open(filename, "w") as file:
        json.dump(data, file, indent=4)

update_daily_records()
