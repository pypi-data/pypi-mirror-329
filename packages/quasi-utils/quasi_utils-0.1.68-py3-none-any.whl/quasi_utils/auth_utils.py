import json
import os
from hashlib import blake2b, sha256
from http.cookies import SimpleCookie

import jwt
from jwt.exceptions import PyJWTError

ACAO, ACAC = 'Access-Control-Allow-Origin', 'Access-Control-Allow-Credentials'


def validate_jwt(encoded_jwt, secret):
	try:
		return 200, jwt.decode(encoded_jwt, secret, algorithms='HS256')
	except PyJWTError as e:
		return 401, str(e)


def read_cookie(cookie, cookie_name):
	cookie = SimpleCookie(cookie)
	
	return cookie[cookie_name].value


def origin_verification(headers):
	allowed_origins = ['http://localhost:5173', 'https://stockemy.in', 'https://oms.stockemy.in']
	origin = headers.get('origin') or headers.get('Origin')
	
	if origin not in allowed_origins:
		code, message, origin = 401, 'Invalid origin', '*'
	else:
		code, message, origin = 200, 'Valid origin', origin
	
	return code, message, origin


def request_verification_flow(headers):
	code, message, origin = origin_verification(headers)
	if code != 200:
		return {'statusCode': code, 'body': json.dumps({'message': message}), 'headers': {ACAO: origin}}
	
	try:
		cookie = headers.get('cookie') or headers.get('Cookie')
		jwt_token = read_cookie(cookie, 'jwt_token')
	except KeyError:
		code, message = 401, 'Missing jwt_token in cookie'
		return {'statusCode': code, 'body': json.dumps({'message': message}), 'headers': {ACAO: origin, ACAC: True}}
	
	code, message = validate_jwt(jwt_token, secret=os.environ['JWT_KEY'])
	if code != 200:
		return {'statusCode': code, 'body': json.dumps({'message': message}), 'headers': {ACAO: origin, ACAC: True}}
	
	return message, origin


def outsiders_verification_flow(oms, event, body, marker):
	path = event['path']
	
	if 'trading_view' in path and str(body['marker']) != str(marker):
		return False
	elif 'kite' in path:
		h = sha256(body['order_id'].encode() + body['order_timestamp'].encode() + oms.api_secret.encode())
		checksum = h.hexdigest()
		
		if checksum != body['checksum']:
			return False
	
	return True


def get_hashed_password(password, key):
	h = blake2b(key=key.encode(), digest_size=16)
	h.update(password.encode())
	
	return h.hexdigest()
