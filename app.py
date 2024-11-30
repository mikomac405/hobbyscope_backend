import os
from flask import Flask, render_template, request, url_for
from appwrite.client import Client
from appwrite.services.account import Account
from dotenv import load_dotenv
load_dotenv()

client = Client()
client.set_endpoint(os.environ.get('ENDPOINT')).set_project(os.environ.get('CLIENT_ID'))


account = Account(client=client)

def updateVerification(user_id, secret):
    try:
       res = account.update_verification(user_id, secret)
       return res
    except Exception as e:
        print(e)
        
def updateNewPassword(user_id, secret, password):
    try:
       res = account.update_recovery(user_id, secret, password)
       return res
    except Exception as e:
        print(e)

app = Flask(__name__)

@app.get("/")
def api():
    return render_template('index.html')

@app.get("/verify")
def verify():
    user_id = request.args.get('userId')
    secret = request.args.get('secret')
    try:
        res = updateVerification(user_id, secret)
        print(res)
        return render_template("template.html", title="✅ Verification Complete", message="Your email address has been verified successfully.");
    except Exception as e:
        return render_template("template.html", title="❌ Verification Failed", message=f"⚠️ Reason : {e}");

@app.get("/recovery")
def recovery():
    user_id = request.args.get('userId')
    secret = request.args.get('secret')
    return render_template("reset_password.html", user_id=user_id, secret=secret, message="")

@app.post("/reset_password")
def reset_password():
    user_id = request.form.get('user_id')
    secret = request.form.get('secret')
    password = request.form.get('password')
    password_confirm = request.form.get('password_confirm')
    
    if password != password_confirm:
        return render_template("reset_password.html", user_id=user_id, secret=secret, message="Passwords do not match.")
    
    if len(password) < 8:
        return render_template("reset_password.html", user_id=user_id, secret=secret, message="Password must be at least 8 characters.")
    
    try:
        res = updateNewPassword(user_id, secret, password)
        print(res)
        return render_template("template.html", title="✅ Password Changed", message="Your password was changed successfully.");
    except Exception as e:
        return render_template("template.html", title="❌ Password Reset Failed", message=f"⚠️ Reason : {e}");
        