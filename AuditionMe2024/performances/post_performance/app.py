import boto3
from boto3.dynamodb.conditions import Key
from os import getenv
from uuid import uuid4

region_name = getenv('APP_REGION')
performances_table = boto3.resource('dynamodb', region_name=region_name ).Table('AuditionMePerformances2024')


def lambda_handler(event, context):
    performance_id = str(uuid4())
    title = event['title']
    director = event['director']
    dates = event['dates']
    available_characters = []
    venue = event['venue']

    if 'available_characters' in event:
        available_characters = event['available_characters']
    
    performance = performances_table.put_item(Item = {
        'performance_id': performance_id,
        'title': title,
        'director': director,
        'dates': dates,
        'current_performances': available_characters,
        'venue': venue
    })
    
    return response(200, { 'id': performance_id, 'performances': performance })

def response(code, body):
    return {
        'status': code,
        'headers': {
            'Content-Type': 'application/json'
            },
        'body': body
    }

my_event = {
    "performance_id": "uuid here",
    "title": "The Cowling Howard",
    "director": "Howard",
    "dates": [
        "8-8-2024",
        "4-4-2024"
    ],
    "available_characters": [
        "Boward the Coward",
        "Loward the Doward"
    ],
    "venue": "Le Noward"
}

lambda_handler(my_event, None)