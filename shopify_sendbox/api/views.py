from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .countries import country_info
import requests
import json
from shopify_sendbox.keys import SENDBOX_AUTHORIZATION_KEY


def get_shipping_quotes(origin_country, origin_state, origin_city, destination_country, destination_state, destination_city, weight):
    url = 'https://live.sendbox.co/shipping/shipment_delivery_quote'
    # Header variables
    authorization_key = SENDBOX_AUTHORIZATION_KEY
    

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
def shipping_rates(request, *args, **kwargs):
    """
    Return Shipping Rates data from SendBox to Shopify Carrier Services API.

    Request body should contain shipping info in json format for the required shipping rates to be calculated. 

    A sample request body is shown below:

            {
                "rate": {
                    "origin": {
                    "country": "Nigeria",
                    "postal_code": "K2P1L4",
                    "province": "LA",
                    "city": "Yaba",
                    "name": null,
                    "address1": "150 Elgin St.",
                    "address2": "",
                    "address3": null,
                    "phone": "16135551212",
                    "fax": null,
                    "email": null,
                    "address_type": null,
                    "company_name": "Jamie D's Emporium"
                    },
                    "destination": {
                    "country": "Ghana",
                    "postal_code": "K1M1M4",
                    "province": null,
                    "city": "Accra",
                    "name": "Bob Norman",
                    "address1": "24 Sussex Dr.",
                    "address2": "",
                    "address3": null,
                    "phone": null,
                    "fax": null,
                    "email": null,
                    "address_type": null,
                    "company_name": null
                    },
                    "items": [{
                    "name": "Short Sleeve T-Shirt",
                    "sku": "",
                    "quantity": 1,
                    "grams": 1000,
                    "price": 1999,
                    "vendor": "Jamie D's Emporium",
                    "requires_shipping": true,
                    "taxable": true,
                    "fulfillment_service": "manual",
                    "properties": null,
                    "product_id": 48447225880,
                    "variant_id": 258644705304
                    },
                    {
                    "name": "Long Sleeve T-Shirt",
                    "sku": "",
                    "quantity": 1,
                    "grams": 4000,
                    "price": 1999,
                    "vendor": "Jamie D's Emporium",
                    "requires_shipping": true,
                    "taxable": true,
                    "fulfillment_service": "manual",
                    "properties": null,
                    "product_id": 48447200880,
                    "variant_id": 258644005304
                    }],
                    "currency": "USD",
                    "locale": "en"
                }
            }



    A sample response for the above request is shown below:

    

            {
                "rates": [
                    {
                        "service_name": "Standard Delivery",
                        "service_code": "standard",
                        "total_price": "9422.0",
                        "description": "Pickup and delivery within 3 - 5 business days",
                        "currency": "USD",
                        "max_delivery_date": "2020-09-18"
                    }
                ]
            }
    """

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
    if not destination_state:
        destination_state = destination_city    

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

