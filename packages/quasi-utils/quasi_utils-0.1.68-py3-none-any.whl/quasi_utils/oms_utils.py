import json
import os
import re
from configparser import ConfigParser

import requests as r
import urllib3
from urllib3.exceptions import InsecureRequestWarning

from quasi_utils.generic_utils import rate_limiter

urllib3.disable_warnings(InsecureRequestWarning)


@rate_limiter
def request(method, url, headers, data=None, params=None, _json=None, timeout=5, verify=False, allow_redirects=True,
            session=None):
	if session:
		res = session.request(method, url, data=data, headers=headers, json=_json, params=params, verify=verify,
		                      allow_redirects=allow_redirects, timeout=timeout, proxies=None)
	else:
		res = r.request(method, url, data=data, headers=headers, json=_json, params=params, verify=verify,
		                allow_redirects=allow_redirects, timeout=timeout, proxies=None)
	
	status_code = res.status_code
	if status_code in [403, 429]:
		print(f'Error {status_code}: {res.text}')
		return {'status_code': status_code}
	
	try:
		return json.loads(res.content.decode('utf8'))
	except json.decoder.JSONDecodeError:
		return res.content


def base(price, rounder=0.05, precision=2):
	return round(rounder * round(float(price) / rounder), precision)


def get_details(config_name, data_dir):
	config = ConfigParser()
	config.read(os.path.join(data_dir, 'config.ini'))
	z = config[config_name]
	api_key, api_secret, access_token = z['api_key'], z['api_secret'], z['access_token']
	
	return api_key, api_secret, access_token


def get_trade_number(orders):
	trade_num = 0
	
	if not orders:
		return trade_num
	
	for order in orders:
		if order['transaction_type'] == 'SELL':
			trade_num += 1
	
	return trade_num


def check_global_loss(o, global_stop_loss):
	margin = o.get_cash_details(verbose=True)
	pnl = margin['utilised']['m2m_realised']
	
	if pnl < 0:
		cash = margin['available']
		total_cash = cash['opening_balance'] + cash['intraday_payin'] + cash['collateral']
		
		return False if abs(pnl) > (total_cash * global_stop_loss) else margin['net']
	
	return margin['net']


def get_total_cash(o):
	margin = o.get_cash_details(verbose=True)
	cash = margin['available']
	
	return cash['opening_balance'] + cash['intraday_payin'] + cash['collateral']


def ticker_transform(ticker):
	months = {'1': 'JAN', '2': 'FEB', '3': 'MAR', '4': 'APR', '5': 'MAY', '6': 'JUN', '7': 'JUL', '8': 'AUG',
	          '9': 'SEP', 'O': 'OCT', 'N': 'NOV', 'D': 'DEC'}
	date_modifier = {'01': 'st', '02': 'nd', '03': 'rd', '21': 'st', '22': 'nd', '23': 'rd'}
	# NIFTY 24 22221150CE
	try:
		cur_year_start_index = re.search(r'\d\d', ticker).start()
	except AttributeError:
		# if the ticker is just a stock ticker and not a future or option
		return ticker
	
	cur_year = ticker[cur_year_start_index: cur_year_start_index + 2]
	_ticker, data = ticker[:cur_year_start_index], ticker[cur_year_start_index + 2:]
	
	if any([x in data for x in months.values()]):
		month, date, strike = data[:3].title(), '', data[3:]
		date_modified = ''
	else:
		month, date, strike = months[data[0]].title(), data[1:3], data[3:]
		date_modified = date_modifier.get(date, 'th')
	
	return f'{_ticker} {date}{date_modified} {month} 20{cur_year} {strike}'


def round_down(x, nearest_num=50):
	return x if x % nearest_num == 0 else x - (x % nearest_num)


def round_up(x, nearest_num=50):
	return x if x % nearest_num == 0 else x + (nearest_num - (x % nearest_num))
