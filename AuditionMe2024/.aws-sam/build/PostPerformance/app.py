import boto3
from boto3.dynamodb.conditions import Key
from os import getenv
from uuid import uuid4
import json

region_name = getenv('APP_REGION')
performances_table = boto3.resource('dynamodb', region_name=region_name).Table('AuditionMePerformances2024')

def lambda_handler(event, context):

    body = event['body']

    performance_id = str(uuid4())
    title = body['title']
    director = body['director']
    venue = body['venue']
    dates = []
    auditions_open = body['auditions_open']
    available_characters = []
    audition_list = []
    
    if 'dates' in body:
        dates = body['dates']

    if 'available_characters' in body:
        available_characters = body['available_characters']

    if 'audition_list' in body:
        audition_list = body['audition_list']

    performance = {
        'performance_id': performance_id,
        'title': title,
        'director': director,
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

# my_event = {
#     "title": "The Cowling Howard",
#     "director": "500d0a82-50f9-4d84-abee-507eac387090",
#     "venue": "Le Noward",
#     "dates": [
#         "8-8-2024",
#         "4-4-2024"
#     ],
#     "auditions_open": True,
#     "available_characters": [
#         "Boward the Coward",
#         "Loward the Doward"
#     ]
# }

# lambda_handler(my_event, None)