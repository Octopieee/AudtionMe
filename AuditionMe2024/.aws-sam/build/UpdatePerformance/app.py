import boto3
from boto3.dynamodb.conditions import Key
from os import getenv
from uuid import uuid4
import json

region_name = getenv('APP_REGION')
performances_table = boto3.resource('dynamodb', region_name=region_name ).Table('AuditionMePerformances2024')

def lambda_handler(event, context):
    performance_id = event['performance_id']
    title = event['title']
    director_id = event['director']
    venue = event['venue']
    dates = event['dates']
    auditions_open = event['auditions_open']
    available_characters = event['available_characters']
    audition_list = event['audition_list']
    
    if 'director_id' not in event or performance_id is None:
        response(400, "ID is required!")

    performance = performances_table.get_item(Key = { 'performance_id': performance_id })['Item']

    if performance is None:
        response(404, "Person not found!")

    if title is not None:
        performance['title'] = title

    if director_id is not None:
        performance['director'] = director_id

    if venue is not None:
        performance['venue'] = venue
    
    if dates is not None and isinstance(dates, list):
        performance['dates'] = dates

    if auditions_open is not None:
        performance['auditions_open'] = auditions_open

    if available_characters is not None and isinstance(available_characters, list):
        performance['available_characters'] = available_characters

    if audition_list is not None and isinstance(audition_list, list):
        audition_list = event['audition_list']

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

# my_event = {S
#     "performance_id": "uuid here",
#     "title": "The Cowling Howard",
#     "director": "Howard",
#     "dates": [
#         "8-8-2024",
#         "4-4-2024"
#     ],
#     "available_characters": [
#         "Boward the Coward",
#         "Loward the Doward"
#     ],
#     "venue": "Le Noward"
# }

# print(lambda_handler(my_event, None))
