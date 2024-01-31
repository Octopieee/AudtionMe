import boto3
from boto3.dynamodb.conditions import Key
from os import getenv
from uuid import uuid4
import json

region_name = getenv('APP_REGION')
performances_table = boto3.resource('dynamodb', region_name=region_name ).Table('AuditionMePerformances2024')
performers_table = boto3.resource('dynamodb', region_name=region_name ).Table('AuditionMePerformers2024')

def lambda_handler(event, context):
    performance_id = event['performance_id']
    performer_id = event['performer_id']

    if performance_id is None:
        return response(400, "Performance ID wasn't found!")
    
    if performer_id is None:
        return response(400, "Performer ID wasn't found!")

    performance = performances_table.get_item(Key = { 'performance_id': performance_id })['Item']
    performer = performers_table.get_item(Key = { 'performer_id': performer_id })

    if performance is None:
        return response(404, "Performance wasn't found!")
    
    if performer is None:
        return response(404, "Performer wasn't found!")

    performance['audition_list'].remove(performer_id)

    performer['current_performances'].append(performance_id)

    performances_table.put_item(Item = performance)
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

my_event = {
    'test_event': 'hi :D'
}

print(lambda_handler(my_event, None))
