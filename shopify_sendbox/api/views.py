from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import requests
import json
from .keys import *


def get_shipping_quotes(origin_country, origin_state, origin_city, destination_country, destination_state, destination_city, weight):
    url = 'https://live.sendbox.co/shipping/shipment_delivery_quote'
    # Header variables
    authorization_key = sendbox_authorization_key

    content_type = 'application/json'

    # # Body variables
        # origin_country = 'Nigeria'    
        # origin_state = 'Lagos'     
        # origin_city = 'Yaba'     
        # destination_country = 'Nigeria'     
        # destination_state = 'Abuja'     
        # destination_city = 'Kuje'     
        # weight = float('3')

    payload = {
        'origin_country': origin_country,  
        'origin_state': origin_state,
        'origin_city': origin_city,   
        'destination_country': destination_country,      
        'destination_state': destination_state,     
        'destination_city': destination_city,    
        'weight': weight
    }

    headers = {
        'Authorization': authorization_key,
        'Content-type': content_type
    }

    response = requests.post(url, data=json.dumps(payload), headers=headers)
    if response.status_code == 201:
        return json.loads(response.content)['rates']
    return None


@api_view(['POST'])
def shipping_rates(request):
    """
    Return Shipping Rates data from SendBox to Shopify Carrier Services API
    """
    post_data = request.data
    total_shipping_price = 0.0
    # Parse required variables from incoming POST request
    for item in post_data['items']:
        origin_country = post_data['origin']['country']    
        origin_state = post_data['origin']['province']     
        origin_city = post_data['origin']['city']     
        destination_country = post_data['destination']['country']      
        destination_state = post_data['destination']['province']     
        destination_city = post_data['destination']['city']     
        weight = float(item['grams'])/1000

        # Get shipping rates
        shipping_data = get_shipping_quotes(
            origin_country, origin_state, origin_city, destination_country, destination_state, destination_city, weight
        )
        if not shipping_data:
            return Response({'errors': 'Request Data Values/Format Invalid'}, status=status.HTTP_400_BAD_REQUEST)
        rate = shipping_data[0]
        total_shipping_price += rate['fee']

    # Create response with shipping rates data
    response = []
    body = {
        "service_name": rate['name'],
        "service_code": rate['code'],
        "total_price": str(int(total_shipping_price)),
        "description": rate['description'],
        "currency": "USD",
        "max_delivery_date": rate['delivery_eta'][:10]
    }
    response.append(body)

    return Response(response, status=status.HTTP_201_CREATED)

