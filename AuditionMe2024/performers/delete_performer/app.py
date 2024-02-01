import boto3
from boto3.dynamodb.conditions import Key
from os import getenv
from uuid import uuid4
import json

region_name = getenv('APP_REGION')
performers_table = boto3.resource('dynamodb', region_name=region_name ).Table('AuditionMePerformers2024')

def lambda_handler(event, context):
    if 'pathParameters' not in event:
        return response(400, "No path parameters found!")
    
    path_params = event['pathParameters']

    if path_params is None or 'performer_id' not in path_params:
        return response(400, "No ID was found in path parameters!")
    
    performer_id = path_params['performer_id']

    performers_table.delete_item(Key = { 'performer_id': performer_id })

    return response(200, None)

def response(code, body):
    return {
        'statusCode': code,
        'headers': {
            'Content-Type': 'application/json'
            },
        'body': json.dumps(body),
        "isBase64Encoded": False
    }

# my_event = {
#     'test_event': 'hi :D'
# }

# print(lambda_handler(my_event, None))
