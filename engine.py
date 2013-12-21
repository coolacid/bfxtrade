#!/usr/bin/env python

from bitfinex import *
import json

# Targets
starget = 20.00 # Set High
btarget = 16.00 # Set Low

# Ignore orders outside these numbers
lignore = 10 # Lower Then
hignore = 30 # Higher Then

ltcleave = 24.9625	# Amount to leave in LTC
ltctobuy = 25.00		# Amount to Trade with Bot

bfx = Bitfinex()
bfx.secret = ''
bfx.key = ''

# Check to see how much LTC I have
for balance in bfx.balances():
    if balance['currency'] == 'ltc' and balance['type'] == 'exchange':
	currentb = float(balance['amount'])

if currentb == ltcleave:
    print "Buying: Checking to see if we already have an order."
    dontbuy = False
    for order in  bfx.orders():
	#print order
	if order['price'] < lignore or order['price'] > hignore:
	    print "Ignoring order: %d for %f " % (order['id'], order['price']) 
	else:
	    print "We have Order: %d, %f for %f, nothing todo." %(order['id'], order['remaining_amount'], order['price'])
	    dontbuy = True
    if dontbuy == False:
	print "We are going to buy %f LTC for %f" % (ltctobuy, btarget)
	payload = {}
	payload['symbol'] = 'ltcusd'
	payload['amount'] = str(ltctobuy)
	payload['price'] = str(btarget)
	payload['exchange'] = 'all'
	payload['side'] = 'buy'
	payload['type'] = 'exchange limit'
	border = bfx.order_new(payload)
	print border
else:
    print "Selling: Checking to see if we already have an order."
    dontsell = False
    for order in  bfx.orders():
	if order['price'] < lignore or order['price'] > hignore:
	    print "Ignoring order: %d for %f " % (order['id'], order['price']) 
	else:
	    print "We have Order: %f, nothing todo." %(order['price'])
	    dontsell = True
    if dontsell == False:
	samount = currentb - ltcleave
	print "We are going to sell %f LTC for %f" % (ltctobuy, starget)
	payload = {}
	payload['symbol'] = 'ltcusd'
	payload['amount'] = str(samount)
	payload['price'] = str(starget)
	payload['exchange'] = 'all'
	payload['side'] = 'sell'
	payload['type'] = 'exchange limit'
	border = bfx.order_new(payload)
	print border



