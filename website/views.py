import requests
from django.shortcuts import redirect
from django.urls import reverse
import logging
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def canva_callback(request):
    code = request.GET.get('code')
    if not code:
        return redirect(reverse('wagtailadmin_home'))  # Redirect if no code is present

    token_url = "https://www.canva.com/api/oauth/token"
    data = {
        'grant_type': 'authorization_code',
        'client_id': os.getenv('CANVA_CLIENT_ID'),
        'client_secret': os.getenv('CANVA_CLIENT_SECRET'),
        'code': code,
        'redirect_uri': os.getenv('CANVA_REDIRECT_URI'),
        'code_verifier': os.getenv('CANVA_CODE_VERIFIER')
    }

    # Send POST request to exchange the code for an access token
    response = requests.post(token_url, data=data)
    token_data = response.json()

    # Log the full token data response
    logging.info(f"Canva Token Response: {token_data}")

    access_token = token_data.get('access_token')
    if not access_token:
        logging.error(f"Failed to retrieve access token. Response: {token_data}")
        return redirect(reverse('wagtailadmin_home'))

    # Log the access token if it was retrieved successfully
    logging.info(f"Access Token: {access_token}")

    # Proceed with the token (store it or use it for API requests)
    return redirect(reverse('wagtailadmin_home'))
