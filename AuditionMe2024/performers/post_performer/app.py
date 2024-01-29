import boto3
from boto3.dynamodb.conditions import Key
from os import getenv
from uuid import uuid4
import json

region_name = getenv('APP_REGION')
performers_table = boto3.resource('dynamodb', region_name=region_name ).Table('AuditionMePerformers2024')


def lambda_handler(event, context):
    performer_id = str(uuid4())
    name = event['name']
    email = event['email']
    number = event['number']
    current_performances = []
    past_performances = []

    if 'current_performances' in event:
        current_performances = event['current_performances']
    
    if 'past_performances' in event:
        past_performances = event['past_performances']
    
    performer = performers_table.put_item(Item = {
        'performer_id': performer_id,
        'name': name,
        'email': email,
        'number': number,
        'current_performances': current_performances,
        'past_performances': past_performances
    })
    
    return response(200, { 'id': performer_id, 'performer': performer })

def response(code, body):
    return {
        'statusCode': code,
        'headers': {
            'Content-Type': 'application/json'
            },
        'body': json.dumps(body)
    }

my_event = {
    'name': 'Coward',
    'email': 'coward@gmail.com',
    'number': '111-111-1111'
}

lambda_handler(my_event, None)