import boto3
from boto3.dynamodb.conditions import Key
from os import getenv
from uuid import uuid4, UUID
import json

region_name = getenv('APP_REGION')
performances_table = boto3.resource('dynamodb', region_name=region_name ).Table('AuditionMePerformances2024')

def lambda_handler(event, context):
    performance_id = str(uuid4())
    title = event['title']
    director_id = event['director']
    venue = event['venue']
    dates = []
    auditions_open = event['auditions_open']
    available_characters = []
    audition_list = []
    
    if 'dates' in event and isinstance(dates, list):
        dates = event['dates']

    if 'available_characters' in event and isinstance(available_characters, list):
        available_characters = event['available_characters']

    if 'audition_list' in event and isinstance(audition_list, list):
        audition_list = event['audition_list']

    performance = {
        'performance_id': performance_id,
        'title': title,
        'director': director_id,
        'venue': venue,
        'dates': dates,
        'auditions_open': auditions_open,
        'available_characters': available_characters,
        'audition_list': audition_list
    }
    
    performances_table.put_item(Item = performance)
    
    return response(200, performance)

def response(code, body):
    return {
        'statusCode': code,
        'headers': {
            'Content-Type': 'application/json'
            },
        'body': json.dumps(body)
    }

my_event = {
    "title": "The Cowling Howard",
    "director": "500d0a82-50f9-4d84-abee-507eac387090",
    "venue": "Le Noward",
    "dates": [
        "8-8-2024",
        "4-4-2024"
    ],
    "auditions_open": True,
    "available_characters": [
        "Boward the Coward",
        "Loward the Doward"
    ]
}

lambda_handler(my_event, None)