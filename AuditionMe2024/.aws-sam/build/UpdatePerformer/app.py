import boto3
from boto3.dynamodb.conditions import Key
from os import getenv
from uuid import uuid4
import json

region_name = getenv('APP_REGION')
performers_table = boto3.resource('dynamodb', region_name=region_name ).Table('AuditionMePerformers2024')

def lambda_handler(event, context):
    performer_id = event['performer_id']
    name = event['name']
    email = event['email']
    number = event['number']
    current_performances = event['current_performances']
    past_performances = event['past_performances']
    
    if 'performer_id' not in event or performer_id is None:
        response(400, "ID is required!")

    performer = performers_table.get_item(Key = { 'performer_id': performer_id })['Item']

    if performer is None:
        response(404, "Person not found!")

    if name is not None:
        performer['name'] = name

    if email is not None:
        performer['email'] = email
    
    if number is not None:
        performer['number'] = number

    if current_performances is not None and isinstance(current_performances, list):
        performer['current_performances'] = current_performances

    if past_performances is not None and isinstance(past_performances, list):
        performer['past_performances'] = past_performances

    performers_table.put_item(Item = performer)

    return response(200, performer)

def response(code, body):
    return {
        'statusCode': code,
        'headers': {
            'Content-Type': 'application/json'
            },
        'body': json.dumps(body)
    }

# my_event = {
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
