import requests


if __name__ == "__main__":
    print("My IP Address is:",
    requests.get("https://api.ipify.org?format=json").json()['ip']) 