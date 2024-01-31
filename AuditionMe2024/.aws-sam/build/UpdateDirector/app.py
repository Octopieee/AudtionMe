import boto3
from boto3.dynamodb.conditions import Key
from os import getenv
from uuid import uuid4
import json

region_name = getenv('APP_REGION')
directors_table = boto3.resource('dynamodb', region_name=region_name ).Table('AuditionMeDirectors2024')

def lambda_handler(event, context):
    director_id = event['director_id']
    name = event['name']
    email = event['email']
    number = event['number']
    
    if 'director_id' not in event or director_id is None:
        response(400, "ID is required!")

    director = directors_table.get_item(Key = { 'director_id': director_id })['Item']

    if director is None:
        response(404, "Person not found!")

    if name is not None:
        director['name'] = name

    if email is not None:
        director['email'] = email
    
    if number is not None:
        director['number'] = number

    directors_table.put_item(Item = director)

    return response(200, director)

def response(code, body):
    return {
        'statusCode': code,
        'headers': {
            'Content-Type': 'application/json'
            },
        'body': json.dumps(body)
    }

my_event = {
    'test_event': 'hi :D'
}

print(lambda_handler(my_event, None))
