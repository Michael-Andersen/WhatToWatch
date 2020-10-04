import boto3
import json
import bot
from decimal import Decimal

REGION = 'us-west-1'
QUEUE = 'what-to-watch-queue'


def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb', region_name=REGION)
    table = dynamodb.Table('WhatToWatchDB')
    response = table.get_item(Key={'Field': 'acc_num'})
    acc_num = response['Item']['StringValue']
    response2 = table.get_item(Key={'Field': 'consumer_key'})
    consumer_key = response2['Item']['StringValue']
    response3 = table.get_item(Key={'Field': 'consumer_secret'})
    consumer_secret = response3['Item']['StringValue']
    response4 = table.get_item(Key={'Field': 'access_token'})
    access_token = response4['Item']['StringValue']
    response5 = table.get_item(Key={'Field': 'access_token_secret'})
    access_token_secret = response5['Item']['StringValue']
    queue_url = f'https://sqs.{REGION}/{acc_num}/{QUEUE}'
    api = bot.config(consumer_key, consumer_secret,
                     access_token, access_token_secret)
    response6 = table.get_item(Key={'Field': 'since_id'})
    since_id = response6['Item']['NumericalValue']
    since_id, mentions = bot.check_mentions(api, ["#"], since_id)
    response7 = table.update_item(
        Key={'Field': 'since_id'},
        UpdateExpression="set NumericalValue=:n",
        ExpressionAttributeValues={
            ':n': Decimal(since_id)
        },
        ReturnValues="UPDATED_NEW"
    )
    sqs = boto3.client('sqs')
    for mention in mentions:
        response = sqs.send_message(
            QueueUrl=queue_url,
            DelaySeconds=10,
            MessageAttributes={
                'user': {
                    'DataType': 'String',
                    'StringValue': mention['user']
                },
                'id': {
                    'DataType': 'String',
                    'StringValue': mention['id']
                },
                'film': {
                    'DataType': 'String',
                    'StringValue': mention['film']
                },
            },
            MessageBody=(
                'Another message'
            )
        )
    return {
        'statusCode': 200,
        'body': json.dumps('Success')
    }