from authenticated_client import AuthenticatedClient;
from SimplePrices import getFills;

with open('auth.txt') as f:
    authInfo = [line.strip() for line in f.readlines() if line.strip()] # [name, key, b64secret, passphrase]

print('\n{:^58}'.format('For ' + authInfo.pop(0))) # prints the user's name

auth_client = AuthenticatedClient(*authInfo[0:3])

def calcAvgPrices(sym):
    fillsGetter = auth_client.get_fills(product_id = sym) # gets the fills from Coinbase Pro (legacy)
    fills = []
    for x in fillsGetter:
        fills.append(x)
    fills.extend(getFills(authInfo[3], authInfo[4], sym))  # adds the fills from Coinbase Advanced
    
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
        if x['side'] in {'buy', 'BUY'}: # buys
            buySum += float(x['size']) * float(x['price'])
            buyTotalSize += float(x['size'])
        else: # sells
            sellSum += float(x['size']) * float(x['price'])
            sellTotalSize += float(x['size'])
    
    return (sym, buySum/buyTotalSize if buyTotalSize else nofillsInd, sellSum/sellTotalSize if sellTotalSize else nofillsInd)

def asStrings(x):
    if isinstance(x, tuple) and len(x) == 3:
        elem1 = x[0]
        elem2 = x[1] if isinstance(x[1], str) else str(round(x[1], 3))
        elem3 = x[2] if isinstance(x[2], str) else str(round(x[2], 3))
        return (elem1, elem2, elem3)
    else:
        raise TypeError('Only works with 3-element tuple (str, float, float)')


with open('syms.txt') as f:
    tickers = [line.strip() for line in f.readlines() if line.strip()] # strips each line and ignores blank lines

lineSep = '\n----------------------------------------------------------\n' # separates each line in the table
print('\nSymbol       Average Buying Price    Average Selling Price', end = lineSep) # table header
for t in tickers:
    x = asStrings(calcAvgPrices(t))
    print('{:10}   {:>20}    {:>21}'.format(x[0], x[1], x[2]), end = lineSep)

input('\n{:^58}\n'.format('Created by Salvatore (2022)'))