import os
from fastapi import FastAPI, HTTPException
import requests

app = FastAPI()

# Okta configuration
OKTA_DOMAIN = "https://dev-21414807.okta.com"
CLIENT_ID = os.environ.get('CLIENT_ID')
CLIENT_SECRET = os.environ.get('CLIENT_SECRET')
TOKEN_URL = f"{OKTA_DOMAIN}/oauth2/default/v1/token"

# Get access token from Okta
def get_access_token():
    response = requests.post(TOKEN_URL, data={
        'grant_type': 'client_credentials',
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'scope': 'custom_scope'
    })
    print(response.text)
    response.raise_for_status()
    return response.json()['access_token']

@app.get("/get-data-from-backend2")
def get_data_from_backend2():
    access_token = get_access_token()
    headers = { 
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get("http://localhost:8001/data", headers=headers)  # Backend 2 URL
    print('response text ', response.text)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Failed to get data from Backend 2")
    return response.json()

# To run this backend:
# uvicorn backend1:app --reload --port 8000
