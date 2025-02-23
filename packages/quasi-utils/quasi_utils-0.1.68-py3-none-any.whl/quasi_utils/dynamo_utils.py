import decimal
import json

import boto3
from boto3.dynamodb.conditions import Key

dy = boto3.resource('dynamodb')


class DecimalEncoder(json.JSONEncoder):
	def default(self, o):
		if isinstance(o, decimal.Decimal):
			return str(o)
		
		return super(DecimalEncoder, self).default(o)


def replace_in_dynamo(table_name, item):
	table = dy.Table(table_name)
	table.put_item(Item=item)


def get_from_dynamo(table_name, key, proj_expr):
	table = dy.Table(table_name)
	res = table.get_item(Key=key, ProjectionExpression=proj_expr)
	
	return res.get('Item')


def update_in_dynamo(table_name, key, update_expr, expr_attr_vals, expr_attr_names=None):
	table = dy.Table(table_name)
	if expr_attr_names is None:
		table.update_item(Key=key, UpdateExpression=update_expr, ExpressionAttributeValues=expr_attr_vals)
	else:
		table.update_item(Key=key, UpdateExpression=update_expr, ExpressionAttributeValues=expr_attr_vals,
		                  ExpressionAttributeNames=expr_attr_names)


def delete_from_dynamo(table_name, key):
	table = dy.Table(table_name)
	table.delete_item(Key=key)


def query_dynamo(table_name, key, proj_expr, expr_attr_names=None):
	table = dy.Table(table_name)
	res = table.query(KeyConditionExpression=key, ProjectionExpression=proj_expr,
	                  ExpressionAttributeNames=expr_attr_names)
	
	return res.get('Items')


def query_gsi_dynamo(table_name, index_name, key, proj_expr):
	table = dy.Table(table_name)
	res = table.query(IndexName=index_name, KeyConditionExpression=Key(key[0]).eq(key[1]),
	                  ProjectionExpression=proj_expr)
	
	return res.get('Items')


# print(query_dynamo('prod_watchlist', Key('user_id').eq('123'), 'list_id, #items',
#                    {'#items': 'items'}))
# print(query_gsi_dynamo('prod_users', 'zerodha_idx', ('zerodha_id', 'QP8623'),
#                        'access_token, api_key, api_secret, marker, zerodha_id'))
