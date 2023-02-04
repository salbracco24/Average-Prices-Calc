#
# cbpro/AuthenticatedClient.py
# Daniel Paquin
#
# For authenticated requests to the Coinbase exchange (get fills only)

import requests
from cbpro_auth import CBProAuth


class AuthenticatedClient():
    """ Provides access to Private Endpoints on the cbpro API.

    All requests default to the live `api_url`: 'https://api.pro.coinbase.com'.
    To test your application using the sandbox modify the `api_url`.

    Attributes:
        url (str): The api url for this client instance to use.
        auth (CBProAuth): Custom authentication handler for each request.
        session (requests.Session): Persistent HTTP connection object.
    """
    def __init__(self, key, b64secret, passphrase,
                 api_url="https://api.pro.coinbase.com"):
        """ Create an instance of the AuthenticatedClient class.
        

        Args:
            key (str): Your API key.
            b64secret (str): The secret key matching your API key.
            passphrase (str): Passphrase chosen when setting up key.
            api_url (Optional[str]): API URL. Defaults to cbpro API.
        """
        self.url = api_url.rstrip('/')
        self.auth = CBProAuth(key, b64secret, passphrase)
        self.session = requests.Session()

    def _send_paginated_message(self, endpoint, params=None):
        """ Send API message that results in a paginated response.

        The paginated responses are abstracted away by making API requests on
        demand as the response is iterated over.

        Paginated API messages support 3 additional parameters: `before`,
        `after`, and `limit`. `before` and `after` are mutually exclusive. To
        use them, supply an index value for that endpoint (the field used for
        indexing varies by endpoint - get_fills() uses 'trade_id', for example).
            `before`: Only get data that occurs more recently than index
            `after`: Only get data that occurs further in the past than index
            `limit`: Set amount of data per HTTP response. Default (and
                maximum) of 100.

        Args:
            endpoint (str): Endpoint (to be added to base URL)
            params (Optional[dict]): HTTP request parameters

        Yields:
            dict: API response objects

        """
        if params is None:
            params = dict()
        url = self.url + endpoint
        while True:
            r = self.session.get(url, params=params, auth=self.auth, timeout=30)
            results = r.json()
            for result in results:
                yield result
            # If there are no more pages, we're done. Otherwise update `after`
            # param to get next page.
            # If this request included `before` don't get any more pages - the
            # cbpro API doesn't support multiple pages in that case.
            if not r.headers.get('cb-after') or \
                    params.get('before') is not None:
                break
            else:
                params['after'] = r.headers['cb-after']

    def get_fills(self, product_id=None, order_id=None, **kwargs):
        """ Get a list of recent fills.

        As of 8/23/18 - Requests without either order_id or product_id
        will be rejected

        This method returns a generator which may make multiple HTTP requests
        while iterating through it.

        Fees are recorded in two stages. Immediately after the matching
        engine completes a match, the fill is inserted into our
        datastore. Once the fill is recorded, a settlement process will
        settle the fill and credit both trading counterparties.

        The 'fee' field indicates the fees charged for this fill.

        The 'liquidity' field indicates if the fill was the result of a
        liquidity provider or liquidity taker. M indicates Maker and T
        indicates Taker.

        Args:
            product_id (str): Limit list to this product_id
            order_id (str): Limit list to this order_id
            kwargs (dict): Additional HTTP request parameters.

        Returns:
            list: Containing information on fills. Example::
                [
                    {
                        "trade_id": 74,
                        "product_id": "BTC-USD",
                        "price": "10.00",
                        "size": "0.01",
                        "order_id": "d50ec984-77a8-460a-b958-66f114b0de9b",
                        "created_at": "2014-11-07T22:19:28.578544Z",
                        "liquidity": "T",
                        "fee": "0.00025",
                        "settled": true,
                        "side": "buy"
                    },
                    {
                        ...
                    }
                ]

        """
        if (product_id is None) and (order_id is None):
            raise ValueError('Either product_id or order_id must be specified.')

        params = {}
        if product_id:
            params['product_id'] = product_id
        if order_id:
            params['order_id'] = order_id
        params.update(kwargs)

        return self._send_paginated_message('/fills', params=params)