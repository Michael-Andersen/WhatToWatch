import bot
import logging
import json
import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)

REGION = 'us-west-1'

def lambda_handler(event, context):
    for record in event['Records']:
        dynamodb = boto3.resource('dynamodb', region_name=REGION)
        table = dynamodb.Table('WhatToWatchDB')
        response2 = table.get_item(Key={'Field': 'consumer_key'})
        consumer_key = response2['Item']['StringValue']
        response3 = table.get_item(Key={'Field': 'consumer_secret'})
        consumer_secret = response3['Item']['StringValue']
        response4 = table.get_item(Key={'Field': 'access_token'})
        access_token = response4['Item']['StringValue']
        response5 = table.get_item(Key={'Field': 'access_token_secret'})
        access_token_secret = response5['Item']['StringValue']
        api = bot.config(consumer_key, consumer_secret,
                         access_token, access_token_secret)
        bot.reply(api,
                  record['messageAttributes']['user']['stringValue'],
                  record['messageAttributes']['id']['stringValue'],
                  record['messageAttributes']['film']['stringValue'])
    return {'statusCode': 200,
            'body': json.dumps(json.dumps('success'))
            }
