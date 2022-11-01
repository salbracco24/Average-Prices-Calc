# Average Prices Calculator

A simple Python script that calculates the average buying and selling prices for various cryptocurrencies traded on Coinbase Pro.

Retrieves data using the [Coinbase Pro API](https://docs.pro.coinbase.com/) (formerly known as
the GDAX)

##### Provided under MIT License by Salvatore Bracco.
*Note: this library may be subtly broken or buggy. The code is released under
the MIT License – please take the following message to heart:*
> THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

## Benefits
- Quickly calculate the average buying and selling prices for cryptocurrencies (similar to how platforms like Fidelity tell you your cost basis and selling price)
- Do not worry about handling the nuances of the API
- Gain an advantage in the market by knowing exactly where you are profitable!

## Under Development
- Unit tests
- Adding Python 3.11 support

## Getting Started
1. Login to Coinbase Pro, and press your profile pic (in the top right corner), then API.
2. Generate a new API key (+ New API Key), with the "View" permission at minimum. *Note your Passphrase and API secret, they are only displayed once.*
3. Document your key, API secret, and passphrase in a file "auth.txt," along with your name, and save it within this directory, as shown below (each element on a separate line):
```
Salvatore Bracco
db70a7f6498dd7f9bcad29d077be779d
xZEo5hAQqdWAA6ZbhI1X9wTsZiZXqikRL9awpCgpRbIGPBfILrbn2lJeeHY7eS9U4z9p5dGus68avl2cLLTkWg==
xhhpas1ijmi
```

4. Install [Python](https://www.python.org/downloads/) 3.9.0.
> Note: This script works on Windows 10 with Python 3.9.0. Other platforms and/or versions are not guaranteed at this time.
5. Install the [Coinbase Pro Python wrapper](https://github.com/danpaquin/coinbasepro-python) by running `pip install cbpro`

### Usage
1. Define the symbols you wish to display in the `syms.txt` file. 
2. Open the `Average Prices Calculator.py` and it should run in a window. Press "enter" to close the window.