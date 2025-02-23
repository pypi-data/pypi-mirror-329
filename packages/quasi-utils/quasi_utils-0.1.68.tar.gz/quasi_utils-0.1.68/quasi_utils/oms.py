import json
from datetime import datetime as dt

from quasi_utils.oms_utils import base, request, ticker_transform


class OMS:
	def __init__(self, decoded_jwt, session=None):
		self.base_url = 'https://api.kite.trade'
		self.api_key, self.access_token = decoded_jwt['api_key'], decoded_jwt['access_token']
		self.api_secret = decoded_jwt.get('api_secret')
		self.headers = {'X-Kite-Version': '3', 'User-Agent': 'Kiteconnect-python/5.0.1',
		                'Authorization': f'token {self.api_key}:{self.access_token}'}
		self.session = session
	
	def ltp(self, tickers):
		if not isinstance(tickers, list):
			tickers = [tickers]
		tickers_ = {'i': tickers}
		
		res = request('GET', f'{self.base_url}/quote/ltp', data=tickers_, params=tickers_,
		              headers=self.headers)
		
		if res.get('status_code') == 403:
			return {'status_code': 403}
		if not res.get('data'):
			return None
		
		return {ticker_.split(':')[-1]: ltp['last_price'] for ticker_, ltp in res['data'].items()}
	
	def quote(self, tickers):
		if not isinstance(tickers, list):
			tickers = [tickers]
		
		res = request('GET', f'{self.base_url}/quote', params={'i': tickers}, headers=self.headers)
		
		if res.get('status_code') == 403:
			return {'status_code': 403}
		if not res.get('data'):
			return None
		
		return res['data']
	
	def get_user(self):
		res = request('GET', f'{self.base_url}/user/profile', headers=self.headers)
		
		if res.get('status_code') == 403:
			return {'status_code': 403}
		
		return res
	
	def get_cash_needed(self, ticker, action, price, qty, price_type, trade_type='MIS', variety='regular',
	                    exchange='NFO'):
		data = {'tradingsymbol': ticker, 'exchange': exchange, 'transaction_type': action, 'price': price,
		        'quantity': qty, 'variety': variety, 'order_type': price_type, 'product': trade_type}
		
		res = request('POST', f'{self.base_url}/margins/orders', headers=self.headers, _json=[data])
		
		if res.get('status_code') == 403:
			return {'status_code': 403}
		if not res.get('data'):
			return res['message']
		
		return res
	
	def get_cash_details(self, verbose=False):
		res = request('GET', f'{self.base_url}/user/margins/equity', headers=self.headers)
		
		if res.get('status_code') == 403:
			return {'status_code': 403}
		if not res.get('data'):
			return res['message']
		
		data = res['data']
		
		return data if verbose else {'cash': round(data['net'], 1), 'pnl': data['utilised']['m2m_realised']}
	
	def get_instruments(self, tickers=None, exchange='NSEd'):
		# this API works without any authentication... lol
		res = request('GET', f'{self.base_url}/instruments/{exchange}', data=None, headers=self.headers)
		
		if isinstance(res, dict) and res.get('status_code') == 403:
			return {'status_code': 403}
		if isinstance(res, dict) and not res.get('data'):
			return None
		
		res = res.decode('utf-8').strip().split('\n')
		header, rows = res[0], res[1:]
		
		# handle special case of sensex index
		data = {'SENSEX': {'token': '265', 'name': 'SENSEX', 'expiry': '', 'strike': '0',
		                   'ticker_type': 'EQ', 'segment': 'INDICES'}} if exchange == 'NSE' else {}
		
		if not tickers:
			for idx, row in enumerate(rows):
				row = row.split(',')
				expiry = dt.strptime(row[5], '%Y-%m-%d') if row[5] != '' else ''
				name = row[3][1:-1]
				
				if name == '' or any(x in name for x in ['-', 'ETF']):
					continue
				
				name = row[2] if exchange == 'NSE' else name
				data[row[2]] = {'token': row[0], 'name': name, 'expiry': expiry, 'strike': row[-6],
				                'ticker_type': row[-3], 'segment': row[-2]}
		
		compare_fn = lambda x: (f"z{x[1]['name']}" if x[1]['name'] != 'NIFTY' else x[1]['name'], x[1]['expiry'])
		data = dict(sorted(data.items(), key=compare_fn))
		
		for ticker, ticker_data in data.items():
			if ticker_data['expiry'] != '':
				ticker_data['expiry'] = dt.strftime(ticker_data['expiry'], '%d %b %Y')
			
			data[ticker] = '|'.join([val for val in data[ticker].values()])
		
		return data
	
	def get_tax_details(self):
		executed_orders = self.get_orders(status='executed')
		
		if isinstance(executed_orders, dict) and executed_orders.get('status_code') == 403:
			return {'status_code': 403}
		if executed_orders is None:
			return None
		
		brokerage, stt, transaction_charges, sebi_charges, stamp_charges, gst = 0, 0, 0, 0, 0, 0
		taxes = {'brokerage': brokerage, 'stt': stt, 'transaction_charges': transaction_charges,
		         'sebi_charges': sebi_charges, 'stamp_charges': stamp_charges, 'gst': gst}
		
		for order in executed_orders:
			if order['status'] not in ['COMPLETED', 'CANCELLED']:
				continue
				
			if order['status'] == 'CANCELLED' and order['filled_qty'] == 0:
				continue
			
			order_value = order['average_price'] * order['filled_qty']
			exchange, trade_type = order['exchange'], order['trade_type']
			
			if exchange == 'NSE' and trade_type == 'DELIVERY':
				brokerage = 0
				stt = 0.1 / 100 * order_value
				transaction_charges = 0.00322 / 100 * order_value
				stamp_charges = 0.015 / 100 * order_value if order['action'] == 'Buy' else 0
			
			elif exchange == 'NSE' and trade_type == 'INTRADAY':
				brokerage = min(0.03 / 100 * order_value, 20)
				stt = 0.025 / 100 * order_value if order['action'] == 'Sell' else 0
				transaction_charges = 0.00322 / 100 * order_value if exchange == 'NSE' else 0.00375 / 100 * order_value
				stamp_charges = 0.003 / 100 * order_value if order['action'] == 'Buy' else 0
			
			elif exchange in ['NFO', 'BFO'] and order['ticker'].split()[-1] == 'FUT':
				brokerage = min(0.03 / 100 * order_value, 20)
				stt = 0.0125 / 100 * order_value if order['action'] == 'Sell' else 0
				transaction_charges = 0.00188 / 100 * order_value if exchange == 'NFO' else 0
				stamp_charges = 0.002 / 100 * order_value if order['action'] == 'Buy' else 0
			
			elif exchange in ['NFO', 'BFO'] and order['ticker'].split()[-1].endswith(('CE', 'PE')):
				brokerage = 20
				stt = 0.1 / 100 * order_value if order['action'] == 'Sell' else 0
				transaction_charges = (0.03553 if exchange == 'NFO' else 0.0325) / 100 * order_value
				stamp_charges = 0.003 / 100 * order_value if order['action'] == 'Buy' else 0
			
			sebi_charges = 0.0001 / 100 * order_value
			gst = 0.18 * (brokerage + sebi_charges + transaction_charges)
			
			taxes['brokerage'] += brokerage
			taxes['stt'] += stt
			taxes['transaction_charges'] += transaction_charges
			taxes['sebi_charges'] += sebi_charges
			taxes['stamp_charges'] += round(stamp_charges)
			taxes['gst'] += gst
		
		taxes['brokerage'] = round(taxes['brokerage'], 2)
		taxes['stt'] = round(taxes['stt'], 2)
		taxes['transaction_charges'] = round(taxes['transaction_charges'], 2)
		taxes['sebi_charges'] = round(taxes['sebi_charges'], 2)
		taxes['stamp_charges'] = round(taxes['stamp_charges'], 2)
		taxes['gst'] = round(taxes['gst'], 2)
		taxes['total_tax'] = round(sum(taxes.values()), 2)
		
		return taxes
	
	def get_positions(self, only_open=False):
		res = request('GET', f'{self.base_url}/portfolio/positions', data=None, headers=self.headers)
		
		if res.get('status_code') == 403:
			return {'status_code': 403}
		if res.get('data') is None:
			return None
		
		positions = res['data']['net']
		
		final_positions = []
		for position in positions:
			temp_position = {'ticker': ticker_transform(position['tradingsymbol']),
			                 'raw_ticker': position['tradingsymbol'],
			                 'exchange': position['exchange'],
			                 'token': position['instrument_token'],
			                 'trade_type': 'OVERNIGHT' if position['product'] == 'NRML' else 'INTRADAY',
			                 'qty': position['quantity'],
			                 'overnight_qty': position['overnight_quantity'],
			                 'avg_price': position['average_price'],
			                 'pnl': position['pnl'],
			                 'm2m': position['m2m'],
			                 'unrealised': position['unrealised'],
			                 'realised': position['realised'],
			                 'day_buy_value': position['day_buy_value'],
			                 'day_sell_value': position['day_sell_value']}
			final_positions.append(temp_position)
		
		return [position for position in final_positions if position['qty']] if only_open else final_positions
	
	def get_orders(self, status='all'):
		res = request('GET', f'{self.base_url}/orders', data=None, headers=self.headers)
		
		if res.get('status_code') == 403:
			return {'status_code': 403}
		if res.get('data') is None:
			return None
		
		orders, open_orders, executed_orders, all_orders = res['data'], [], [], []
		status_values = {'NRML': 'OVERNIGHT', 'MIS': 'INTRADAY', 'CNC': 'DELIVERY', 'COMPLETE': 'COMPLETED'}
		
		for order in orders:
			temp_order = {'order_id': order['order_id'],
			              'status': status_values.get(order['status']) or order['status'],
			              'time': order['order_timestamp'],
			              'variety': order['variety'],
			              'exchange': order['exchange'],
			              'ticker': ticker_transform(order['tradingsymbol']),
			              'raw_ticker': order['tradingsymbol'],
			              'token': order['instrument_token'],
			              'price_type': order['order_type'],
			              'action': order['transaction_type'].title(),
			              'trade_type': status_values[order['product']],
			              'total_qty': order['quantity'],
			              'price': round(order['price'], 2),
			              'average_price': round(order['average_price'], 2),
			              'filled_qty': order['filled_quantity'],
			              'pending_qty': order['pending_quantity']}
			
			if order['meta']:
				is_gtt = order['meta'].get('gtt')
				temp_order['is_gtt'] = True if is_gtt else False
				
				if is_gtt is None:
					temp_order['total_qty'] = order['meta']['iceberg']['total_quantity']
			
			if temp_order['status'] in ['OPEN', 'AMO REQ RECEIVED', 'MODIFY AMO REQ RECEIVED']:
				open_orders.append(temp_order)
			else:
				executed_orders.append(temp_order)
			
			all_orders.append(temp_order)
		
		if status == 'open':
			return open_orders[::-1]
		elif status == 'executed':
			return executed_orders[::-1]
		else:
			return all_orders[::-1]
	
	def place_order(self, ticker, action, price, qty, price_type, trade_type='MIS', variety='regular', exchange='NFO',
	                trigger_price=None, iceberg_legs=None, iceberg_quantity=None, tag=''):
		data = {'tradingsymbol': ticker, 'exchange': exchange, 'transaction_type': action, 'price': price,
		        'quantity': qty, 'variety': variety, 'order_type': price_type, 'product': trade_type,
		        'trigger_price': trigger_price, 'iceberg_legs': iceberg_legs, 'iceberg_quantity': iceberg_quantity,
		        'tag': tag}
		
		res = request('POST', f'{self.base_url}/orders/{variety}', data=data, headers=self.headers)
		
		if res.get('status_code') == 403:
			return {'status_code': 403}
		
		return res
	
	def modify_order(self, order_id=None, price=None, qty=None, price_type=None, variety='regular'):
		data = {}
		if price:
			data['price'] = price
		if qty:
			data['quantity'] = qty
		if price_type:
			data['order_type'] = price_type
		
		res = request('PUT', f'{self.base_url}/orders/{variety}/{order_id}',
		              data=data, headers=self.headers)
		
		if res.get('status_code') == 403:
			return {'status_code': 403}
		
		return res
	
	def cancel_order(self, order_ids, variety='regular'):
		res = {}
		
		order_ids = [order_ids] if not isinstance(order_ids, list) else order_ids
		for _id in order_ids:
			res = request('DELETE', f'{self.base_url}/orders/{variety}/{_id}',
			              headers=self.headers, data=None)
			
			if res.get('status_code') == 403:
				return {'status_code': 403}
			
			res[_id] = res
		
		return res
	
	def get_gtt_orders(self, status='all'):
		res = request('GET', f'{self.base_url}/gtt/triggers', headers=self.headers, data=None)
		
		if res.get('status_code') == 403:
			return {'status_code': 403}
		if res['status'] == 'error':
			return res
		
		orders, open_orders, executed_orders, all_orders = res['data'], [], [], []
		status_values = {'NRML': 'OVERNIGHT', 'MIS': 'INTRADAY', 'CNC': 'DELIVERY',
		                 'triggered': 'TRIGGERRED', 'active': 'ACTIVE'}
		
		for order in orders:
			single_order = order['orders'][0]
			
			temp_order = {'order_id': order['id'],
			              'time': order['created_at'],
			              'status': status_values.get(order['status']) or order['status'],
			              'token': order['condition'].get('instrument_token'),
			              'trade_type': status_values[single_order['product']],
			              'trigger_price': order['condition']['trigger_values'][0],
			              'execution_price': single_order['price'],
			              'exchange': single_order['exchange'],
			              'ticker': ticker_transform(single_order['tradingsymbol']),
			              'raw_ticker': single_order['tradingsymbol'],
			              'price_type': single_order['order_type'],
			              'action': single_order['transaction_type'].title(),
			              'qty': single_order['quantity']}
			
			if temp_order['status'] == 'ACTIVE':
				open_orders.append(temp_order)
			else:
				executed_orders.append(temp_order)
			
			all_orders.append(temp_order)
		
		if status == 'open':
			return open_orders
		elif status == 'executed':
			return executed_orders
		else:
			return all_orders
	
	def place_gtt_order(self, buy_price, trade_type, qty, thresh=1.0, slippage=0.98, ticker=None, prefix=None,
	                    strike=None, exchange='NFO'):
		base_price, ticker = base(buy_price * thresh), ticker or f'{prefix}{strike}'
		
		ltp = self.ltp(f'{exchange}:{ticker}')
		if ltp is None:
			return 'invalid ticker'
		if ltp.get('status_code') == 403:
			return {'status_code': 403}
		
		condition = {'exchange': exchange, 'tradingsymbol': ticker, 'trigger_values': [base_price],
		             'last_price': ltp[ticker]}
		orders = [{'exchange': exchange, 'tradingsymbol': ticker, 'transaction_type': 'SELL', 'quantity': qty,
		           'order_type': 'LIMIT', 'product': trade_type, 'price': base(base_price * slippage)}]
		data = {'condition': json.dumps(condition), 'orders': json.dumps(orders), 'type': 'single'}
		
		res = request('POST', f'{self.base_url}/gtt/triggers', data=data, headers=self.headers)
		
		if res.get('status_code') == 403:
			return {'status_code': 403}
		
		return res
	
	def modify_gtt_order(self, order_id, trigger_price, execution_price, trade_type, qty, ticker, exchange):
		ltp = self.ltp(f'{exchange}:{ticker}')
		if ltp is None:
			return 'invalid ticker'
		if ltp.get('status_code') == 403:
			return {'status_code': 403}
		
		condition = {'exchange': exchange, 'tradingsymbol': ticker, 'trigger_values': [base(trigger_price)],
		             'last_price': ltp[ticker]}
		orders = [{'exchange': exchange, 'tradingsymbol': ticker, 'transaction_type': 'SELL', 'quantity': qty,
		           'order_type': 'LIMIT', 'product': trade_type, 'price': base(execution_price)}]
		data = {'condition': json.dumps(condition), 'orders': json.dumps(orders), 'type': 'single'}
		
		res = request('PUT', f'{self.base_url}/gtt/triggers/{order_id}', data=data, headers=self.headers)
		
		if res.get('status_code') == 403:
			return {'status_code': 403}
		
		return res
	
	def cancel_gtt_order(self, order_ids):
		res = {}
		
		order_ids = [order_ids] if not isinstance(order_ids, list) else order_ids
		for _id in order_ids:
			res = request('DELETE', f'{self.base_url}/gtt/triggers/{_id}',
			              headers=self.headers, data=None)
			if res.get('status_code') == 403:
				return None
			
			res[_id] = res
		
		return res


if __name__ == '__main__':
	obj = OMS({'api_key': '3uggvz253hhhfjnp', 'access_token': 'wAZhTiKRQlPxDLk9e4IQiknrzG0PHqay'})
	# print(obj.access_token)
	# print(obj.ltp(['NSE:RELIANCE']))
	# print(obj.quote(['NSE:RELIANCE']))
	# print(obj.get_user())
	# print(obj.get_cash_needed(exchange='NSE', ticker='RELIANCE', action='BUY', price=2000, qty=1, price_type='LIMIT'))
	# print(obj.get_cash_details())
	# print(obj.get_instruments())
	# print(obj.get_tax_details())
	obj.get_positions()
	# print(obj.get_orders())
	# print(obj.place_order(ticker='RELIANCE', action='BUY', price=2000, qty=1, price_type='LIMIT'))
	# print(obj.modify_order(order_id='231004203471297', price=12.9, qty=500, price_type='LIMIT', variety='amo'))
	# print(obj.cancel_order(order_ids='231004203428841', variety='amo'))
	# print(obj.get_gtt_orders())
	# print(obj.place_gtt_order(buy_price=20, trade_type='MIS', qty=50, thresh=0.9, slippage=0.98,
	#                           ticker='MIDCPNIFTY2490913050PE'))
	
	# print(obj.modify_gtt_order(
	# 	**{"order_id": 237156502, "exchange": "BFO", "ticker": "SENSEX2491381200PE", "qty": 500, "trigger_price": 575,
	# 	   "execution_price": 450, "trade_type": "NRML"}))
	# print(obj.cancel_gtt_order(order_ids=['237156502']))
