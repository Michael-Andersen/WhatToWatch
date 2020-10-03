import bot
import logging
import json
import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    for record in event['Records']:
        s3 = boto3.resource('s3')
        content_object = s3.Object('aws-what-to-watch-json', 'bot.json')
        file_content = content_object.get()['Body'].read().decode('utf-8')
        json_content = json.loads(file_content)
        api = bot.config(json_content['consumer_key'], json_content['consumer_secret'],
                         json_content['access_token'], json_content['access_token_secret'])
        bot.reply(api,
                  record['messageAttributes']['user']['stringValue'],
                  record['messageAttributes']['id']['stringValue'],
                  record['messageAttributes']['film']['stringValue'])
    return {'statusCode': 200,
            'body': json.dumps(json.dumps('success'))
            }
