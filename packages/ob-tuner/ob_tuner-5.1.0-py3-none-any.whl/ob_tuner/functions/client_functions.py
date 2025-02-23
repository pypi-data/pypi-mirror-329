from openbrain.orm.model_client import Client
from ob_tuner.util import logger
import gradio as gr

def save_client_details(email, leadmo_api_key, leadmo_location_id ,leadmo_calendar_id, first_name, last_name, date_of_birth, phone, address1, address2, city, state, country, postal_code, website):
    """Update the client with the latest values from the database"""
    try:
        client = Client(
            email=email,
            leadmo_api_key=leadmo_api_key,
            leadmo_location_id=leadmo_location_id,
            leadmo_calendar_id=leadmo_calendar_id,
            first_name=first_name,
            last_name=last_name,
            date_of_birth=date_of_birth,
            phone=phone,
            address1=address1,
            address2=address2,
            city=city,
            state=state,
            country=country,
            postal_code=postal_code,
            website=website
        )
        client.save()
        gr.Info(f"Successfully updated ")
    except Exception as e:
        gr.Error(f"Please enter your Lead Momentum API key and location ID in order to save.")

def load_client_details(email):
    """Load the client details from the database"""
    try:
        _client = Client.get(email=email)
    except Exception as e:
        gr.Warning(f"Please enter your Lead Momentum API key and location ID, then save your profile to begin using Lead Momentum tools.")
        return ["" for _ in range(14)]
        # _client = Client(email=email, leadmo_api_key="", leadmo_location_id=None, lls_api_key=None)
        # _client.save()

    leadmo_api_key = _client.model_dump().get('leadmo_api_key', "")
    leadmo_location_id = _client.model_dump().get('leadmo_location_id', "")

    leadmo_calendar_id = _client.model_dump().get('leadmo_calendar_id', "")
    first_name = _client.model_dump().get('first_name', "")
    last_name = _client.model_dump().get('last_name', "")
    date_of_birth = _client.model_dump().get('date_of_birth', "")
    phone = _client.model_dump().get('phone', "")
    address1 = _client.model_dump().get('address1', "")
    address2 = _client.model_dump().get('address2', "")
    city = _client.model_dump().get('city', "")
    state = _client.model_dump().get('state', "")
    country = _client.model_dump().get('country', "")
    postal_code = _client.model_dump().get('postal_code', "")
    website = _client.model_dump().get('website', "")

    return [leadmo_api_key, leadmo_location_id, leadmo_calendar_id, first_name, last_name, date_of_birth, phone, address1, address2, city, state, country, postal_code, website]
