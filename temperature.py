import boto3
import json
import os
from datetime import datetime

from decimal import Decimal

dynamodb = boto3.resource('dynamodb')

def post(event, context):
    if event['headers']['x-api-key'] != os.environ['API_KEY']:
        response = {
            "statusCode": 401
        }

        return response

    data = json.loads(event['body'], parse_float=Decimal)
    
    timestamp = datetime.fromisoformat(data['timestamp'])
    temperature = data['temperature']
    humidity = data['humidity']
    room = data['room']

    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    item = {
        'room': room,
        'temperature': temperature,
        'humidity': humidity,
        'updated_at': str(timestamp)
    }

    # write the todo to the database
    table.put_item(Item=item)

    # create a response
    response = {
        "statusCode": 204
    }

    return response
