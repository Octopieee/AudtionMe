import boto3
from boto3.dynamodb.conditions import Key
from os import getenv
from uuid import uuid4
import json

region_name = getenv('APP_REGION')
directors_table = boto3.resource('dynamodb', region_name=region_name ).Table('AuditionMeDirectors2024')

def lambda_handler(event, context):
    if 'pathParameters' in event:
        path_params = event['pathParameters']

        if path_params is None or 'director_id' not in path_params:
            return response(200, directors_table.scan()['Items'])
        
        if path_params is not None and 'director_id' in path_params:
            director_id = path_params['director_id']

            director = directors_table.get_item(Key = { 'director_id': director_id })['Item']

            return response(200, director)
        
    return response(200, directors_table.scan()['Items'])

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
