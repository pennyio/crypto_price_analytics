# XRP Price Data Analytics
Note: This script is a work in progress by Madhu Josyula.  The purpose of this script is to write XRP price/volume and marketcap data to this [spreadsheet].  prices and volumes across different exchanges using their API endpoints.  We will us that data to compare what we believe the *price* and *volume* should be compared to CoinMarketCap, BraveNewCoin, CryptoCompare and BitCoin Averages.

This work is very much in DRAFT, please reach out to [@madhu] if you have any questions about the data or methodology you see below.

### Exchanges
| Exchanges | URL | Currency |
| ------ | ------ | ------ |
| bitbank | https://public.bitbank.cc/xrp_jpy/ticker | JPY |
| Bitcoin Exchange Thailand | https://bx.in.th/api/ | THB |
| Bitcoin Indonesia | https://vip.bitcoin.co.id/api/xrp_btc/ticker | BTC |
| Bitfinex | https://api.bitfinex.com/v1/pubticker/ | BTC , USD |
| bithumb | https://api.bithumb.com/public/ticker/xrp | KRW |
| Bitsane | https://bitsane.com/api/public/ticker | BTC, EUR, USD |
| Bitso | https://api.bitso.com/v3/ticker/?book=xrp_mxn | MXN |
| BitStamp | https://www.bitstamp.net/api/v2/ticker/xrpeur | EUR, USD |
| BTC Markets | https://api.btcmarkets.net/market/XRP/AUD/tick | AUD, BTC |
| BTC38 | http://api.btc38.com/v1/ticker.php?c=xrp | CNY |
| BTCX India | https://m.btcxindia.com/api/ticker | INR |
| BTER BTC | http://data.bter.com/api2/1/tickers | BTC |
| BTER CNY | http://data.bter.com/api2/1/tickers | CNY |
| Coinone | https://api.coinone.co.kr/ticker/?currency=xrp&format=json | KRW |
| Cryptomate | https://cryptomate.co.uk/api/XRP/ | GBP |
| Hit-BTC | http://api.hitbtc.com/api/1/public/XRPBTC/ticker | BTC |
| Jubi | http://www.jubi.com/api/v1/ticker/?coin=xrp | CNY |
| Korbit | https://api.korbit.co.kr/v1/ticker/detailed?currency_pair=xrp_krw | KRW | 
| Kraken CAD | https://api.kraken.com/0/public/Ticker?pair=XRPCAD | CAD, EUR, JPY, USD |
| Poloniex BTC | https://poloniex.com/public?command=returnTicker&currencyPair=ALL | BTC, USDT |
| XRP Ledger | https://data.ripple.com/v2/exchange_rates | XRP |
| YuanBao | https://www.yuanbao.com/api_market/getinfo_cny/coin/xrp | CNY |

### Indexes
| Indexes | URL |
| ------ | ------ |
| CMC | https://api.coinmarketcap.com/v1/ticker/ripple/?convert=USD |
| CryptoCompare | https://min-api.cryptocompare.com/data/pricemultifull?fsyms=XRP&tsyms=USD |
| Bitcoin Averages | https://apiv2.bitcoinaverage.com/indices/global/ticker/XRPUSD |

   [@madhu]: <https://github.com/madhujosyula>
   [spreadsheet]: <https://docs.google.com/spreadsheets/d/1oM_-u8rh_a7HhDGkwRNP0i7CMdcG4-ay64qD7e-mJws/edit#gid=0>


					