# Shopify-SendBox-Integration-API
An API for calculating shipping rates for Shopify accounts. It recevies request formatted for the Shopify Carrier Services API and then parses the info to get the required shipping rates from SendBox's API and returns it in the response.

## It is particularly useful for Shopify accounts with a delivery base in Africa and Asia and parts of Europe
This is so because the shipping rates returned are exact rates the Shopify merchant will spend on shipping the particular items with the available shipping info. This eliminates discrepancy between what the merchant collects from the client during online checkout and what the merchant actually pays Sendbox to ship.

## API Documentation
https://shopify-sendbox.herokuapp.com/api/v1/doc/

![API screenshot 1](doc_screenshots/Screenshot4.png?raw=true)

![API screenshot 2](doc_screenshots/Screenshot5.png?raw=true)
#### *TL; DR* - Screenshots of API documentation


The documentation can also be accessed in JSON format through:
https://shopify-sendbox.herokuapp.com/api/v1/doc.json

and in YAML format through:
https://shopify-sendbox.herokuapp.com/api/v1/doc.yaml


## API Endpoint
https://shopify-sendbox.herokuapp.com/api/v1/sendboxrate
