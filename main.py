import requests
import datetime as dt
import os

GENDER = "MALE"
WEIGHT_KG = "97"
HEIGHT = "185.5"
AGE = "30"

APP_ID = f"{os.environ['APP_ID']}"
API_KEY = f"{os.environ['API_KEY']}"

endpoint_url = "https://trackapi.nutritionix.com/v2/natural/exercise"
sheet_endpoint = f"{os.environ['sheet_endpoint']}"

exercise_input = input("Tell which exercise you did today?: ")

header = {
    "x-app-id": APP_ID,
    'x-app-key': API_KEY,
}

parameters = {
    'query': exercise_input,
    "gender": GENDER,
    "weight_kg": WEIGHT_KG,
    "height_cm": HEIGHT,
    "age": AGE,
}

response = requests.post(url=endpoint_url, json=parameters, headers=header)
response.raise_for_status()
result = response.json()
print(result)


bearer_headers = {
"Authorization": f"{os.environ['Authorization']}"
}

today_date = dt.datetime.now().strftime("%d/%m/%Y")
now_time = dt.datetime.now().strftime("%X")
for exercise in result["exercises"]:
    sheet_inputs = {
        "workout": {
            "date": today_date,
            "time": now_time,
            "exercise": exercise['name'].title(),
            "duration": exercise['duration_min'],
            "calories": exercise['nf_calories'],
        }
    }
    sheet_response = requests.post(sheet_endpoint, json=sheet_inputs, headers=bearer_headers)

    print(sheet_response.text)