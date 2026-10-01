import json
from datetime import datetime

def update_daily_records(cal, carbs, fat, protein):
    filename = "record.json"
    dt_now = str(datetime.now().date())
    #print(dt_now)

    with open(filename, "r") as file:
        data = json.load(file)
                    
    data[dt_now + "cal"] = cal
    data[dt_now + "carbs"] = carbs
    data[dt_now + "fat"] = fat
    data[dt_now + "protein"] = protein

    with open(filename, "w") as file:
        json.dump(data, file, indent=4)

