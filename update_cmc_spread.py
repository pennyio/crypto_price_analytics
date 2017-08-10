#!/usr/bin/env python
#encoding: utf-8
#
# @author Madhu Josyula, mjosyula@gmail.com
# @date 2017-06-01
#
# @details
# My attempt at replicating CMC data in a google spreadsheet
# Spreadsheet: https://docs.google.com/spreadsheets/d/1oM_-u8rh_a7HhDGkwRNP0i7CMdcG4-ay64qD7e-mJws/edit#gid=0

#Imports
from oauth2client.service_account import ServiceAccountCredentials
from bs4 import BeautifulSoup

import json
import requests
import gspread
import datetime, time
import os

#Functions
def getJSON(exch,url):
    start_time = time.time()
    header = {'x-requested-with': 'XMLHttpRequest'}
    mainPage = requests.get(url, headers = header)
    data = mainPage.json()
    print('%s API Query finished in %s seconds') % (exch, str(round(time.time() - start_time,2)))
    return data

def indexPos(exchange_name,row_type):
    a = exchange_name + row_type
    return 'C' + str(main.find(a).row)

def pricePos(sht,exchange_name):
    sht_name = ws.worksheet(sht)
    return 'D' + str(sht_name.find(exchange_name).row)

def volumePos(sht,exchange_name):
    sht_name = ws.worksheet(sht)
    return 'E' + str(sht_name.find(exchange_name).row)

def getValue(data,layer):
    if layer in ('IGNORE'):
        return 0
    else:
        a = data
        alist = layer.split(",")
        for i in xrange(len(alist)):
            a = a.get(alist[i])

        if isinstance(a,list):
            a = a[0]

        return str(a).replace(",","")

def updateSpread(exch,price,vol,price_curr,vol_curr):
    price_update_xrp = str('=iferror(round(%s * GoogleFinance("CURRENCY:%sUSD"),5),"")') % (str(price),price_curr)
    price_update_native = str('=iferror(%s,"")') % (str(price))
   
    if vol_curr in ('XRP'):
        price_xrp = str('round(%s * GoogleFinance("CURRENCY:%sUSD"),5)') % (str(price),price_curr)
        volume_update = str('=iferror(%s * %s,"")') % (str(vol),str(price_xrp))
    else:
        volume_update = str('=iferror(%s * GoogleFinance("CURRENCY:%sUSD"),"")') % (str(vol),str(vol_curr))

    xrp_sheet = ws.worksheet("XRP Price Data")
    xrp_sheet.update_acell(pricePos("XRP Price Data",exch), price_update_xrp)    
    xrp_sheet.update_acell(volumePos("XRP Price Data",exch), volume_update)
    
    fx_sheet = ws.worksheet("Implied FX Rates Data")
    fx_sheet.update_acell(pricePos("Implied FX Rates Data",exch), price_update_native)    
    fx_sheet.update_acell(volumePos("Implied FX Rates Data",exch), volume_update)
    
    return None

def updateMKT(exch,price,vol,mkt,price_curr,vol_curr,mkt_curr):    
    iprice_update = str('=iferror(round(%s * GoogleFinance("CURRENCY:%sUSD"),5),"")') % (str(price),price_curr)
    ivolume_update = str('=iferror(round(%s * GoogleFinance("CURRENCY:%sUSD"),2),"")') % (str(vol),price_curr)
    imkt_cap_update = str('=iferror(round(%s * GoogleFinance("CURRENCY:%sUSD"),2),"")') % (str(mkt),price_curr)

    main = ws.worksheet("XRP Price Data")
    main.update_acell(indexPos(exch," Price"),   iprice_update)
    main.update_acell(indexPos(exch," Volume"),  ivolume_update)
    main.update_acell(indexPos(exch," Market Cap"), imkt_cap_update)
    return None

#Auth for Google Sheets
scope = ['https://spreadsheets.google.com/feeds']
creds = ServiceAccountCredentials.from_json_keyfile_name('/Users/madhu/iPython/client_secret.json', scope)
client = gspread.authorize(creds)

ws = client.open("DRAFT | XRP Price")

#Update Time on Spreadsheet
now = datetime.datetime.now()
updated = "Last Updated at " + now.strftime("%Y-%m-%d %H:%M %p")

main = ws.worksheet("XRP Price Data")
main.update_acell('B1',updated)


#Update Exchange Prices and Volumes
info = ws.worksheet("Exchange Information")

for x in range(3,len(set(info.col_values(2)))+1,1):
    try:
        #read from sheet
        exch = info.cell(x,2).value
        url  = info.cell(x,4).value
        price_layer = info.cell(x,5).value
        vol_layer = info.cell(x,6).value
        price_curr = info.cell(x,7).value
        vol_curr = info.cell(x,8).value
        
        #get JSON from APIs
        data = getJSON(exch,url)

        #extract price and volume data
        price = getValue(data,price_layer)
        vol = getValue(data,vol_layer)

        #update spreadsheet

        updateSpread(exch,price,vol,price_curr,vol_curr)

    except ValueError:
        print "%s - API Not Responding" % exch

#Update Index Price, Volumes and Market Cap
info = ws.worksheet("Index Information")
main = ws.worksheet("XRP Price Data")

for x in range(3,len(set(info.col_values(2)))+1,1):
    try:
        #read from sheet
        exch = info.cell(x,2).value
        url  = info.cell(x,3).value
        price_layer = info.cell(x,4).value
        vol_layer = info.cell(x,5).value
        mkt_layer = info.cell(x,6).value
        vol_curr = info.cell(x,7).value
        price_curr = info.cell(x,8).value
        mkt_curr = info.cell(x,9).value
        
        #get JSON from APIs
        data = getJSON(exch,url)

        #extract price and volume data
        if exch in ('CMC'):
            price = getValue(data[0],price_layer)
            vol = getValue(data[0],vol_layer)
            mkt = getValue(data[0],mkt_layer)
        else:
            price = getValue(data,price_layer)
            vol = getValue(data,vol_layer)
            mkt = getValue(data,mkt_layer)
        #update spreadsheet
        updateMKT(exch,price,vol,mkt,price_curr,vol_curr,mkt_curr)   

    except ValueError:
        print "%s - API Not Responding" % exch

#Ripple Data
info = ws.worksheet("Index Information")
main = ws.worksheet("XRP Price Data")

try:
    xrp_data = getJSON("XRPCharts Price","https://data.ripple.com/v2/exchange_rates/XRP/USD+rvYAfWj5gh67oV6fW32ZzP3Aw4Eubs59B")
    ext_mkts = getJSON("XRPCharts External Volume","https://data.ripple.com/v2/network/external_markets")
    xrpl_mkts = getJSON("XRPCharts XRPL Volume","https://data.ripple.com/v2/network/exchange_volume")
    eth_price_data = getJSON("CMC Ether","https://api.coinmarketcap.com/v1/ticker/ethereum/?convert=USD")

    price = xrp_data["rate"]
    eth_price = eth_price_data[0]["price_usd"]

    data_xrp_dist = getJSON("XRPCharts Market Cap","https://data.ripple.com/v2/network/xrp_distribution?descending=true&limit=1")
    dist = data_xrp_dist["rows"][0]['total']

    ripple_mkt_cap = str('=round(%s * %s,2)') % (str(price),str(dist))

    main.update_acell(indexPos("XRPCharts"," Market Cap"), ripple_mkt_cap)

    #XRP On-Ledger Volume
    xrpl_mkt_str = "=0"

    for x in range(0,len(xrpl_mkts["rows"][0]["components"]),1):

        amt = xrpl_mkts["rows"][0]["components"][x]["amount"]

        if xrpl_mkts["rows"][0]["components"][x]["base"]["currency"] in ('XRP'):
            amt_usd = float(price) * float(amt)
            xrpl_mkt_str = xrpl_mkt_str + " + " + str(amt_usd)
        elif xrpl_mkts["rows"][0]["components"][x]["base"]["currency"] in ('ETH'):
            amt_usd = float(eth_price) * float(amt)
            xrpl_mkt_str = xrpl_mkt_str + " + " + str(amt_usd)
        else:
            fx_rate = str('GoogleFinance("CURRENCY:%sUSD")') % str(xrpl_mkts["rows"][0]["components"][x]["base"]["currency"])
            xrpl_mkt_str = xrpl_mkt_str + str(" + IFERROR(%s*%s,0)") % ( str(amt), fx_rate)
    
    main.update_acell(volumePos("XRP Price Data","XRP Ledger"), xrpl_mkt_str)
    
    #XRPCharts External Volume
    ext_mkt_vol = 0
    for x in range(0,len(ext_mkts["data"]["components"]),1):
        ext_mkt_vol = ext_mkt_vol + float(ext_mkts["data"]["components"][x]["base_volume"])

    ext_mkt_update = xrpl_mkt_str + " + " + str(ext_mkt_vol * float(price))
    
    main.update_acell(indexPos("XRPCharts"," Volume"), ext_mkt_update)
  
except (KeyError, ValueError):
    print "Ripple API Not Responding"

