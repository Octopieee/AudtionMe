import boto3
from boto3.dynamodb.conditions import Key
from boto3.dynamodb.conditions import Attr
from os import getenv
from uuid import uuid4
import json
import re
from base64 import b64encode, b64decode

region_name = getenv('APP_REGION')
directors_table = boto3.resource('dynamodb', region_name=region_name ).Table('AuditionMeDirectors2024')

def lambda_handler(event, context):
    # Fetch authorization header
    auth_header = event['headers']["Authorization"]
    is_allow = "Deny"

    # Use a regex pattern on header
    m1 = re.match("^Basic (.+)$", auth_header)

    # Base 64 decode our encrypted creds
    creds = b64decode(m1[1])

    # Match it again but in bytes
    m2 = re.match(br"^([^:]+):(.+)$", creds)

    # Decode from bytes to utf-8
    name = m2[1].decode('utf-8')
    email = m2[2].decode('utf-8')

    # Filter directors database table by name and email
    director = directors_table.scan(FilterExpression=Attr('name').eq(name) & Attr('email').eq(email))

    if director is not None:
        print(f'User {name} found in db')
        is_allow = "Allow"
    else:
        print("User not found in db")
    
    response = {
        "principalId": f'abcd',
        "policyDocument": {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Action": "execute-api:Invoke",
                    "Effect": is_allow,
                    "Resource": event['methodArn']
                }
            ]
        },
        "context": {
            "exampleKey": "exampleValue"
        }
    }

    return response