from flask import Flask, redirect, request
import requests
import urllib.parse
import os

CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
REDIRECT_URL = os.getenv("REDIRECT_URL")

app = Flask(__name__)

@app.route('/login')
def login():
    scope = "user-read-email user-read-private user-top-read"
    auth_url = (
        "https://accounts.spotify.com/authorize?"
        + urllib.parse.urlencode({
            "client_id": CLIENT_ID,
            "response_type": "code",
            "redirect_uri": REDIRECT_URL,
            "scope": scope,
        })
    )
    return redirect(auth_url)

@app.route("/callback")
def callback():
    code = request.args.get("code")

    token_resp = requests.post(
        "https://accounts.spotify.com/api/token",
        data={
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": REDIRECT_URL,
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
        }
    )
    token_resp.raise_for_status()
    tokens = token_resp.json()

    app.config['USER_TOKEN'] = tokens["access_token"]
    app.config['REFRESH_TOKEN'] = tokens.get("refresh_token")
    app.config['TOKEN_TYPE'] = tokens.get("token_type")

    return tokens 

@app.route("/user_token")
def user_token():
    return {"access_token": app.config.get("USER_TOKEN")}

@app.route("/refresh_token")
def refresh_token():
    return {"refresh_token": app.config.get("REFRESH_TOKEN")}

if __name__ == "__main__":
    app.run(port=5000, debug=True)