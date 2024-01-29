import boto3
from boto3.dynamodb.conditions import Key
from os import getenv
from uuid import uuid4

region_name = getenv('APP_REGION')
directors_table = boto3.resource('dynamodb', region_name=region_name ).Table('AuditionMeDirectors2024')

def lambda_handler(event, context):
    if 'pathParameters' not in event:
        return response(400, { "Error": "No path parameters found!" })
    
    path_params = event['pathParameters']

    if path_params is None or 'id' not in path:
        return response(400, "No ID was found in path parameters!")
    
    director_id = path_params['director_id']

    director = directors_table.delete_item(Key = { 'director_id': director_id })

    return response(200, { 'director_id': director_id, 'director': director })

def response(code, body):
    return {
        'status': code,
        'headers': {
            'Content-Type': 'application/json'
            },
        'body': body
    }

my_event = {
    'test_event': 'hi :D'
}

print(lambda_handler(my_event, None))
