from datetime import datetime
import requests
import schedule
import time
from twilio.rest import Client

ACCOUNT_SID=""
AUTH_TOKEN=""

client = Client(ACCOUNT_SID,
                AUTH_TOKEN)


def send_email():
	def create_session_info(center, session):
	    return {"name": center["name"],
             "date": session["date"],
             "capacity": session["available_capacity"],
             "pincode": center["pincode"],
             "age_limit": session["min_age_limit"]}

	def get_sessions(data):
		for center in data["centers"]:
			for session in center["sessions"]:
				yield create_session_info(center, session)

	def is_available(session):
		return session["capacity"] > 0

	def is_eighteen_plus(session):
		return session["age_limit"] == 18


# in the params variable add your pincode in the "pincode": ___

	def get_for_seven_days(start_date):
		url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin"
		params = {"pincode": your pincode, "date": start_date.strftime("%d-%m-%Y")}
		headers = {
			"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0"}
		resp = requests.get(url, params=params, headers=headers)
		data = resp.json()
		return [session for session in get_sessions(data) if is_eighteen_plus(session) and is_available(session)]

	def create_output(session_info):
		return f"Pincode: {session_info['pincode']}\nOn date: {session_info['date']} - {session_info['name']} has a capacity of ({session_info['capacity']}) slots available."

	print(get_for_seven_days(datetime.today()))
	content = "\n\n".join([create_output(session_info)
                        for session_info in get_for_seven_days(datetime.today())])
	if not content:
		print("No availability")
	else:
            message = client.messages.create(
            	body=content, from_="whatsapp:add the twilio whatsapp no. you get ", to="whatsapp:the whatsapp number you used to send message to twilio sendbox")


schedule.every(0.2).minutes.do(send_email)

while True:
	schedule.run_pending()
	time.sleep(1)
