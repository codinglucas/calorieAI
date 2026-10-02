import json
from datetime import datetime

def check_keys(data, dt, filename):

    column_names = [f"{dt}cal", f"{dt}carbs", f"{dt}fat", f"{dt}protein", "counter"]

    for x in column_names:
        if x in data:
            continue
        else:
            data[x] = 0;

    with open(filename, "w") as file:
        json.dump(data, file, indent=4)




def update_daily_records(cal, carbs, fat, protein):
    filename = "record.json"
    dt_now = str(datetime.now().date())

    try:
        with open(filename, "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        print(f"{filename} not found. Creating a new template.")
        data = {}  
    except json.JSONDecodeError:
        print(f"{filename} is corrupted or empty.")
        data = {}

    check_keys(data, dt_now, filename)
                    
    data[dt_now + "cal"] = data[dt_now + "cal"] + cal
    data[dt_now + "carbs"] = data[dt_now + "carbs"] + carbs
    data[dt_now + "fat"] = data[dt_now + "fat"] + fat
    data[dt_now + "protein"] = data[dt_now + "protein"] + protein

    with open(filename, "w") as file:
        json.dump(data, file, indent=4)

def update_test_data(cal, carbs, fat, protein):
    filename = "performance_data.json"
    dt_now = str(datetime.now().date())

    try:
        with open(filename, "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        print(f"{filename} not found. Creating a new template.")
        data = {}  
    except json.JSONDecodeError:
        print(f"{filename} is corrupted or empty.")
        data = {}

    check_keys(data, dt_now, filename)
                    
    data[dt_now + "cal"] = data[dt_now + "cal"] + cal
    data[dt_now + "carbs"] = data[dt_now + "carbs"] + carbs
    data[dt_now + "fat"] = data[dt_now + "fat"] + fat
    data[dt_now + "protein"] = data[dt_now + "protein"] + protein
    data["counter"] = data["counter"] + 1

    with open(filename, "w") as file:
        json.dump(data, file, indent=4)

if __name__ == "__main__":
    pass