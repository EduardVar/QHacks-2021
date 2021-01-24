# QHacks-2021

## For frontend

`cd 'house-aggregator/client'`
`npm install`
`vue serve`

We sadly didn't get around to intergrating a front end for users :(

## For backend

`cd 'house-aggregator'
`pip install -r requirements.txt'
`python -m server`

Visit `127.0.0.1/all` to see the server scrap 5 different housing sites and display the results. (It takes a while :P)

Made with code and <3

## For Machine Learning

You can predict the price of a house using command line arguments

`python ml/predict_price.py a b c d`

Where:
* a is distance to campus (ex: 10 minutes)
* b is date posted in ddmmyyyy (ex: 15012021)
* c is number of bedrooms
* d is number of bathrooms

~~Note: you might have to `pip install sklearn`~~
