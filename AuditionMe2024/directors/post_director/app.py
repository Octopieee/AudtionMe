import boto3
from boto3.dynamodb.conditions import Key
from os import getenv
from uuid import uuid4
import json

region_name = getenv('APP_REGION')
directors_table = boto3.resource('dynamodb', region_name=region_name ).Table('AuditionMeDirectors2024')

def lambda_handler(event, context):
    director_id = str(uuid4())
    name = event['name']
    email = event['email']
    number = event['number']
    
    director = {
        'director_id': director_id,
        'name' : name,
        'email' : email,
        'number' : number
    }
    
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

# my_event = {
#     'name': 'Howard',
#     'email': 'howard@gmail.com',
#     'number': '801-801-8018'
# }

# lambda_handler(my_event, None)
