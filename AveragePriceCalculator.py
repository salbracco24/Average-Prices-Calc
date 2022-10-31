import cbpro

auth_client = cbpro.AuthenticatedClient("ea756e2bb49d2a89e4aef6b238b05319",
                                       "F6krWqaIqcO2P7R+WRvLMV2WzWIMOd4oEu50y7tDwNdNWyTQvIGQTvKxygDK/4MJWsKeyhAQKfTMtvn40kCI2g==",
                                       "eeg4jyop58q")

def calcAvgPrices(sym):
    fillsGetter = auth_client.get_fills(product_id = sym)
    fills = []
    for x in fillsGetter:
        fills.append(x)
    
    nofillsInd = "--------" # no fills indicator
    errorInd = "ERROR" # error indicator
    if not fills: # no fills found for that product_id
        return (sym, nofillsInd, nofillsInd)
    if fills[0] == 'message': # error (probably invalid product_id)
        return (sym, errorInd, errorInd)
    
    buySum = 0 # weighted sum for buys
    buyTotalSize = 0 # sum of sizes for buys
    sellSum = 0 # weighted sum for sells
    sellTotalSize = 0 # sum of sizes for sells
    
    for x in fills:
        if x['side'] == 'buy': # buys
            buySum += float(x['size']) * float(x['price'])
            buyTotalSize += float(x['size'])
        else: # sells
            sellSum += float(x['size']) * float(x['price'])
            sellTotalSize += float(x['size'])
    
    return (sym, buySum/buyTotalSize if buyTotalSize else nofillsInd, sellSum/sellTotalSize if sellTotalSize else nofillsInd)

def asStrings(x):
    if isinstance(x, tuple) and len(x) == 3:
        elem1 = x[0]
        elem2 = x[1] if isinstance(x[1], str) else str(round(x[1], 2))
        elem3 = x[2] if isinstance(x[2], str) else str(round(x[2], 2))
        return (elem1, elem2, elem3)
    else:
        raise TypeError('Only works with 3-element tuple (str, float, float)')


tickers_old = ['BTC-USD','ETH-USD','BCH-USD','LTC-USD','MATIC-USD','SOL-USD','SHIT-USD']
tickers = ['ADA-USD', 'ALGO-USD', 'ATOM-USD', 'AVAX-USD', 'BAT-USD', 'BCH-USD', 
'BTC-USD', 'BUSD-USD', 'CRV-USD', 'DOGE-USD', 'DOT-USD', 'Dai-USD', 
'ETC-USD', 'ETH-USD', 'FIL-USD', 'LINK-USD', 'LTC-USD', 'MANA-USD', 
'MATIC-USD', 'OMG-USD', 'SHIB-USD', 'SOL-USD', 'XLM-USD', 'XTZ-USD']

lineSep = '\n----------------------------------------------------------\n' # separates each line in the table
print('\nSymbol       Average Buying Price    Average Selling Price', end = lineSep) # table header
for t in tickers:
    x = asStrings(calcAvgPrices(t))
    print('{:10}   {:>20}    {:>21}'.format(x[0], x[1], x[2]), end = lineSep)