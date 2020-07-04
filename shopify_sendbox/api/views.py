from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import requests
import json
from .keys import *
from .countries import country_info


def get_shipping_quotes(origin_country, origin_state, origin_city, destination_country, destination_state, destination_city, weight):
    url = 'https://live.sendbox.co/shipping/shipment_delivery_quote'
    # Header variables
    authorization_key = sendbox_authorization_key

    content_type = 'application/json'
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
        return json.loads(response.content)
    return None


@api_view(['POST'])
def shipping_rates(request):
    """
    Return Shipping Rates data from SendBox to Shopify Carrier Services API
    """
    # if "rate" in request.data:
        # if 'origin' in request.data['rate'] and 'destination' in request.data['rate']:
        #     post_data = request.data['rate']
        #     response = {
        #         "rates": [
        #             {
        #                 "service_name": country_info[post_data['destination']['country']],
        #                 "service_code": "standard",
        #                 "total_price": post_data['items'][0]['grams'],
        #                 "description": post_data['destination']['province'],
        #                 "currency": "USD",
        #                 "max_delivery_date": "2020-07-11"
        #             }
        #         ]
        #     }

        #     return Response(response, status=status.HTTP_201_CREATED)

    post_data = request.data['rate']
    total_shipping_price = 0.0
    
    # Parse required variables from incoming POST request
    origin_country = post_data['origin']['country']
    # Convert Country Code to full for SendBox API
    if len(origin_country) == 2:
        origin_country = country_info[origin_country]    
    origin_state = post_data['origin']['province']     
    origin_city = post_data['origin']['city']     
    destination_country = post_data['destination']['country']
    # Convert Country Code to full for SendBox API
    if len(destination_country) == 2:
        destination_country = country_info[destination_country]      
    destination_state = post_data['destination']['province']     
    destination_city = post_data['destination']['city']     
    

        # Get shipping rates
    for item in post_data['items']:
        weight = float(item['grams'])/1000
        shipping = get_shipping_quotes(
            origin_country, origin_state, origin_city, destination_country, destination_state, destination_city, weight
        )
        if not shipping:
            return Response({'errors': 'Request Data Values/Format Invalid'}, status=status.HTTP_400_BAD_REQUEST)
        rate = shipping['rates'][0]
        total_shipping_price += rate['fee']

    # Create response with shipping rates data
    response = {
        "rates": [
            {
                "service_name": rate['name'],
                "service_code": rate['code'],
                "total_price": str(total_shipping_price // 4.07), # convert to USD for shopify
                "description": rate['description'],
                "currency": "USD",
                "max_delivery_date": rate['delivery_eta'][:10]
            }
        ]
    }

    return Response(response, status=status.HTTP_201_CREATED)

