import requests
import random

def send_verification_email(email):
    code = random.randint(100000, 999999)
    text = f"email: {email}\ncode: {code}"
    
    TOKEN = "7496528180:AAGkAUPuZV3QCsd1svipSL6gcnC0x1sghlA"
    CHAT_ID = "-4743756923"

    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    params = {"chat_id": CHAT_ID, "text": text}

    response = requests.get(url, params=params)
    return code


from .models import User

print(User.objects.all())