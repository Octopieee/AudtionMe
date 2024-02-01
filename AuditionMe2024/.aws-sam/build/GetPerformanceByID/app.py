import boto3
from boto3.dynamodb.conditions import Key
from os import getenv
from uuid import uuid4
import json

region_name = getenv('APP_REGION')
performances_table = boto3.resource('dynamodb', region_name=region_name ).Table('AuditionMePerformances2024')

def lambda_handler(event, context):
    if 'pathParameters' in event:
        path_params = event['pathParameters']

        if path_params is None or 'performance_id' not in path_params:
            return response(200, performances_table.scan()['Items'])
        
        if path_params is not None and 'performance_id' in path_params:
            performance_id = path_params['performance_id']

            performance = performances_table.get_item(Key = { 'performance_id': performance_id })['Item']

            if performance is None:
                performance = performances_table.get_item(Key = { 'director': performance_id })['Item']

            return response(200, performance)
        
    return response(200, performances_table.scan()['Items'])

def response(code, body):
    return {
        'statusCode': code,
        'headers': {
            'Content-Type': 'application/json'
            },
        'body': json.dumps(body)
    }

# my_event = {
#     'test_event': 'hi :D'
# }

# print(lambda_handler(my_event, None))
