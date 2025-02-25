# `FlexfillsApi`

The `FlexfillsApi` is a package for using Flex Fills WebSocket communication with FlexFills trading services.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install FlexfillsApi.

```bash
pip install FlexfillsApi
```

## Usage

```python
import FlexfillsApi

# initialize FlexfillsApi, returns authenticated FlexfillsApi Object
flexfills_api = FlexfillsApi.initialize('username', 'password', is_test=True)

# get assets list
assets_list = flexfills_api.get_asset_list()

# get instruments list
assets_list = flexfills_api.get_instrument_list()
```

### Available Functions

<table class="table table-bordered">
    <thead class="thead-light">
        <tr>
            <th>Functions</th>
            <th>Params</th>
            <th>Explaination</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><code class="highlighter-rouge">get_asset_list()</code></td>
            <td></td>
            <td>Provides a list of supported assets and their trading specifications.</td>
        </tr>
        <tr>
            <td><code class="highlighter-rouge">get_instrument_list()</code></td>
            <td></td>
            <td>Provides a list of supported Instruments and their trading specifications.</td>
        </tr>
        <tr>
            <td><code class="highlighter-rouge">subscribe_order_books(instruments, callback=None)</code></td>
            <td><p><strong>instruments:</strong> list of pair of currencies. All available pairs are:</p>
            <code class="highlighter-rouge">BTC/PLN, DASH/PLN, EUR/GBP, LTC/GBP, LTC/USD, OMG/EUR, OMG/PLN, USDT/EUR, XRP/USD, ZEC/BTC, ZEC/PLN, ZRX/BTC, DOT/BTC, ZRX/USD, BSV/USDT, ADA/USDT, ZIL/USDT, ENJ/USD, XEM/USDT, BNB/USDT, BSV/EUR, BTC/EUR, DASH/EUR, LINK/USD, LTC/ETH, ZEC/USD, BAT/USDT, DOT/USDT, DOT/ETH, MATIC/USTD, AVAX/USDT, BAT/EUR, BAT/GBP, BCH/BTC, BTC/USDT, ETH/GBP, EUR/USD, LINK/BTC, LINK/ETH, LTC/EUR, LTC/USDT, USDT/GBP, XEM/USD, XLM/ETH, XRP/ETH, DASH/USDT, DASH/ETH, XTZ/USD, DAI/USD, ADA/USD, DOT/EUR, BAT/USD, BCH/USDC, BSV/USD, BTC/GBP, DASH/BTC, LTC/PLN, USDT/USD, XLM/BTC, XRP/PLN, ZRX/PLN, QTUM/USDT, ADA/USDC, USDT/USDC, QTUM/USD, MKR/USD, SOL/USD, ATOM/ETH, ATOM/USDT, QASH/USD, VRA/USD, BCH/ETH, BSV/PLN, BTC/USD, ETH/BTC, LTC/BTC, OMG/USD, USDC/EUR, USDC/USD, USDC/USDT, XEM/BTC, XLM/EUR, XLM/USD, XRP/EUR, BSV/ETH, XLM/USDT, ZEC/USDT, BAT/USDC, LINK/USDC, SOL/BTC, DOGE/USD, DOGE/BTC, BAT/BTC, BAT/PLN, BCH/GBP, BCH/PLN, BCH/USD, BTC/USDC, ETH/USDC, OMG/BTC, BTC-PERPETUAL, ETH-PERPETUAL, ZRX/EUR, ADA/BTC, QTUM/ETH, DOT/USD, SOL/ETH, ATOM/BTC, ETH/USDT, EUR/PLN, LINK/PLN, LINK/USDT, OMG/ETH, XRP/BTC, XRP/USDT, ZEC/EUR, ADA/EUR, ADA/PLN, DOT/PLN, OMG/USDT, EUR/USDT, DOGE/USDT, GALA/USDT, BAT/ETH, BCH/EUR, BCH/USDT, BSV/BTC, DASH/USD, ETH/EUR, ETH/PLN, ETH/USD, GBP/USD, USD/PLN, XLM/PLN, XRP/GBP, ZIL/USD, USDT/PLN, XRP/USDC, QTUM/BTC, ADA/ETH, ZIL/BTC, SOL/USDT, LUNA/USDT, ATOM/USD</code>
            <p><strong>callback:</strong> Callback function for getting streaming data.</p>
            </td>
            <td>Provides streaming services an order book for selected symbol, user needs to provide levels of order book to receive. MAX is 20. MIN is 1. Order books are sorted based on NBBO price: BIDs best (Max) first then descending, ASKs best (MIN) first then ascending. The whole Order books is updated every 20MS regardless of changes.</td>
        </tr>
        <tr>
            <td><code class="highlighter-rouge">unsubscribe_order_books(instruments)</code></td>
            <td><strong>instruments:</strong> list of pair of currencies.</td>
            <td></td>
        </tr>
        <tr>
            <td><code class="highlighter-rouge">trade_book_public(instruments, callback=None)</code></td>
            <td>
                <p><strong>instruments:</strong> list of pair of currencies.</p>
                <p><strong>callback:</strong> Callback function for getting streaming data.</p>
            </td>
            <td>Provides streaming services a trading book (public trades) for selected symbol. Once subscribed updates will be pushed to user as they appear at FlexFills.</td>
        </tr>
        <tr>
            <td><code class="highlighter-rouge">get_balance(currencies)</code></td>
            <td><strong>currencies:</strong> list of selected currencies.</td>
            <td></td>
        </tr>
        <tr>
            <td><code class="highlighter-rouge">get_private_trades(instruments, callback=None)</code></td>
            <td>
                <p><strong>instruments:</strong> list of pair of currencies.</p>
                <p><strong>callback:</strong> Callback function for getting streaming data.</p>
            </td>
            <td>Private trades subscription will provide a snapshot of currently open ACTIVE orders and then updates via WebSocket.</td>
        </tr>
        <tr>
            <td><code class="highlighter-rouge">get_open_orders_list(instruments)</code></td>
            <td>
                <p><strong>instruments:</strong> list of pair of currencies. optional</p>
            </td>
            <td>Get current list of open orders. One time request/response.</td>
        </tr>
        <tr>
            <td><code class="highlighter-rouge">create_order(order_datas)</code></td>
            <td>
                <p><strong>order_datas:</strong> The list of order data dict. The order data includes globalInstrumentCd, clientOrderId, orderType, timeInForce, price, amount, exchangeName, orderSubType, tradeSide
                <ul>
                    <li>globalInstrumentCd - pair of currencies (BTC/USD, ...). string</li>
                    <li>clientOrderId: Id of the order. string</li>
                    <li>orderType: <strong>market</strong> - Market order, <strong>limit</strong> - Limit order. string</li>
                    <li>timeInForce: string, optional, 
                        <ul>
                            <li><strong>GTC</strong> - Good till cancelled (default, orders are in order book for 90 days)</li>
                            <li><strong>GTD</strong> - Good till day, will terminate at end of day 4:59PM NY TIME</li>
                            <li><strong>GTT</strong> - Good till time, alive until specific date (cannot exceed 90 days)</li>
                            <li><strong>FOK</strong> - Fill or Kill, Fill full amount or nothing immediately</li>
                            <li><strong>IOC</strong> - Immediate or Cancel, Fill any amount and cancel the rest immediately</li>
                        </ul>
                    </li>
                    <li>price: optional, Price only required for limit orders</li>
                    <li>amount: Quantity of the order</li>
                    <li>exchange: Name of exchange to send order to, string, required</li>
                    <li>orderSubType: optional, string, POST_ONLY, only required if client wishes to submit a passive order which does not immediately fill the order, in case of immediate fill, order will be rejected</li>
                    <li>tradeSide: optional, string, Side of the order Enum buy or sell</li>
                </ul>
                </p>
            </td>
            <td>Get current list of open orders. One time request/response.</td>
        </tr>
        <tr>
            <td><code class="highlighter-rouge">cancel_order(order_datas)</code></td>
            <td>
                <p><strong>order_datas:</strong> The list of order data dict. The order data includes globalInstrumentCd, clientOrderId, direction, orderType, timeInForce, price, amount, exchange
                <ul>
                    <li>globalInstrumentCd - pair of currencies (BTC/USD, ...). string, required</li>
                    <li>clientOrderId: Id of the order. string, required</li>
                    <li>orderType: <strong>market</strong> - Market order, <strong>limit</strong> - Limit order. string, required</li>
                    <li>direction: Side of the order Enum "BUY", "SELL" and "POST_ONLY". string, required</li>
                    <li>timeInForce: string, required</li>
                    <li>price: Price only required for limit orders, string, required</li>
                    <li>amount: Quantity of the order, string, required</li>
                    <li>exchange: Name of exchange to send order to. string, required</li>
                </ul>
                </p>
            </td>
            <td>User may cancel existing orders; client may cancel one order by either including orderId or exchangeOrderId if orderId is not known. Only one parameter is needed and will be accepted. If no orderId or transactionId are added in the message than, all orders for selected pair/s will be cancelled. Must be subscribed to valid pair in order to cancel order in proper pair!</td>
        </tr>
        <tr>
            <td><code class="highlighter-rouge">modify_order(order_data)</code></td>
            <td>
                <p><strong>order_data:</strong> The dict of order data, including globalInstrumentCd, clientOrderId or exchangeOrderId
                <ul>
                    <li>globalInstrumentCd - pair of currencies (BTC/USD, ...). string</li>
                    <li>clientOrderId: Id of the account. string</li>
                    <li>exchangeOrderId: clientOrdId. string</li>
                    <li>price: If price is not passed in, then it’s not modified, string</li>
                    <li>amount: If price is not passed in, then it’s not modified, string</li>
                </ul>
                </p>
            </td>
            <td>Clients may update existing orders. Amount or Price can be modified. Client must use clientOrderId or exchangeOrderId Only one parameter is needed and will be accepted</td>
        </tr>
        <tr>
            <td><code class="highlighter-rouge">get_trade_history(date_from, date_to, instruments)</code></td>
            <td>
                <p><strong>date_from:</strong> Start date of required time frame, string. example: "2022-12-01T00:00:00"</p>
                <p><strong>date_to:</strong> End date of required time frame, string. example: "2022-12-31T00:00:00"</p>
                <p><strong>instruments:</strong> list of pair of currencies.</p>
            </td>
            <td>Clients may request a list <strong>PARTIALLY_FILLED</strong>, <strong>FILLED</strong> trades for a required time frame. Channel arguments ‘date-from’, ‘date-to’ are optional. If ‘date-from’ is not provided, it will be defaulted to ‘now minus 24 hours’. If ‘date-to’ is not provided, it will be defaulted to ‘now’.</td>
        </tr>
        <tr>
            <td><code class="highlighter-rouge">get_order_history(date_from, date_to, instruments, statues)</code></td>
            <td>
                <p><strong>date_from:</strong> Start date of required time frame, string. example: "2022-12-01T00:00:00"</p>
                <p><strong>date_to:</strong> End date of required time frame, string. example: "2022-12-31T00:00:00"</p>
                <p><strong>instruments:</strong> list of pair of currencies.</p>
                <p><strong>statues:</strong> list of status.</p>
            </td>
            <td>Clients may request a list of <strong>COMLETED</strong>, <strong>REJECTED</strong>, <strong>PARTIALLY_FILLED</strong>, <strong>FILLED</strong>, <strong>EXPIRED</strong> order requests for a required time frame. Channel arguments ‘date-from’, ‘date-to’, ‘status’ are optional. If ‘date-from’ is not provided, it will be defaulted to ‘now minus 24 hours’. If ‘date-to’ is not provided, it will be defaulted to ‘now’. If ‘status‘ is not provided then trades with any status will be selected.</td>
        </tr>
        <tr>
            <td><code class="highlighter-rouge">get_trade_positions()</code></td>
            <td></td>
            <td></td>
        </tr>
        <tr>
            <td><code class="highlighter-rouge">trades_data_provider(exchange, instrument, period, timestamp, candle_count)</code></td>
            <td>
                <p><strong>exchange:</strong> Name of exchange. string, required</p>
                <p><strong>instrument:</strong> pair of currencies (BTC/USD, ...). string, required</p>
                <p><strong>period:</strong> period can be <strong>ONE_MIN</strong>, <strong>FIVE_MIN</strong>, <strong>FIFTEEN_MIN</strong>, <strong>THIRTY_MIN</strong>, <strong>FORTY_FIVE_MIN</strong>, <strong>ONE_HOUR</strong>, <strong>TWO_HOUR</strong>, <strong>FOUR_HOURS</strong>, <strong>TWELVE_HOURS</strong>, <strong>ONE_DAY</strong></p>
                <p><strong>timestamp:</strong> Timestamp. string, required</p>
                <p><strong>candle_count:</strong> The number of candles to get. integer, required</p>
            </td>
            <td></td>
        </tr>
        <tr>
            <td><code class="highlighter-rouge">get_exchange_names()</code></td>
            <td>
                <p><strong>exchange:</strong> Name of exchange. string, required</p>
                <p><strong>instrument:</strong> pair of currencies (BTC/USD, ...). string, required</p>
                <p><strong>period:</strong> period can be <strong>ONE_MIN</strong>, <strong>FIVE_MIN</strong>, <strong>FIFTEEN_MIN</strong>, <strong>THIRTY_MIN</strong>, <strong>FORTY_FIVE_MIN</strong>, <strong>ONE_HOUR</strong>, <strong>TWO_HOUR</strong>, <strong>FOUR_HOURS</strong>, <strong>TWELVE_HOURS</strong>, <strong>ONE_DAY</strong></p>
                <p><strong>candle_count:</strong> The number of candles to get. integer, required</p>
            </td>
            <td></td>
        </tr>
        <tr>
            <td><code class="highlighter-rouge">get_instruments_by_type(exchange, instrument_type)</code></td>
            <td>
                <p><strong>exchange:</strong> Name of exchange. string, required</p>
                <p><strong>instrument_type:</strong> string, required</p>
            </td>
            <td></td>
        </tr>
    </tbody>
</table>

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)
