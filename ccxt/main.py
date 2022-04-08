import ccxt_engine as ce

ccxt_engine = ce.CCXTEngine(2022, 2022, 'BTC/IDR', True)
ccxt_engine.load_data()
