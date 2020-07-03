from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import requests
import json


def get_shipping_quotes(origin_country, origin_state, origin_city, destination_country, destination_state, destination_city, weight):
    url = 'https://live.sendbox.co/shipping/shipment_delivery_quote'
    # Header variables
    authorization_key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzZW5kYm94LmF1dGgiLCJhaWQiOiI1ZWM4MTY2NDBlZDU0MjAwMWUyZDMzMmUiLCJ0d29fZmEiOmZhbHNlLCJ1aWQiOiI1ZGIwNGVlMTNjMDQzYjAwNGE3YTYxOWQiLCJleHAiOjE2MDAwMDUwNTR9.n5EM-W9si0nGAlSbjTTaIhJ6iKsjIY3X2uuBOul-X_g'

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
    return "NOT 201"


@api_view(['POST'])
def shipping_rates(request):
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
        rate = shipping_data[0]
        total_shipping_price += rate['fee']

    # Create response with shipping rates data
    response = []
    body = {
        "service_name": rate['name'],
        "service_code": rate['code'],
        "total_price": str(int(total_shipping_price)),
        "description": rate['description'],
        "currency": "NGN",
        "max_delivery_date": rate['delivery_eta'][:10]
    }
    response.append(body)

    return Response(response, status=status.HTTP_201_CREATED)

    

