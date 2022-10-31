import cbpro

auth_client = cbpro.AuthenticatedClient("ea756e2bb49d2a89e4aef6b238b05319",
                                       "F6krWqaIqcO2P7R+WRvLMV2WzWIMOd4oEu50y7tDwNdNWyTQvIGQTvKxygDK/4MJWsKeyhAQKfTMtvn40kCI2g==",
                                       "eeg4jyop58q")

def calcAvgPrices(sym):
    fillsGetter = auth_client.get_fills(product_id = sym)
    fills = []
    for x in fillsGetter:
        fills.append(x)
    print(fills)

# calcAvgPrices('ETH-BTC')

prices = [('MATIC-USD', 10.52, 1057.53), ('ALGO-USD', 2000.23, 500.117), ('SHIT-USD', "ERROR", "ERROR"), ('BTC-USD', "--------", "--------")]

print('\n\u0332Symbol       Average Buying Price    Average Selling Price')
print('----------------------------------------------------------')
for x in prices:
    if isinstance(x[1], str):
        print('{:10}   {:>20}    {:>21}'.format(x[0], x[1], x[2]))
        print('----------------------------------------------------------')
    else:
        print('{:10}   {:20.2f}    {:21.2f}'.format(x[0], x[1], x[2]))
        print('----------------------------------------------------------')