import bot
import logging
import json
import boto3


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def lambda_handler(event, context):
    s3 = boto3.resource('s3')
    content_object = s3.Object('aws-what-to-watch-json', 'bot.json')
    file_content = content_object.get()['Body'].read().decode('utf-8')
    json_content = json.loads(file_content)
    if json_content['locked']:
        return {'statusCode': 200,
                'body': json.dumps(json.dumps('skipping because other lambda running'))
               }
    else:
        json_content["locked"] = True
        api = bot.config(json_content['consumer_key'], json_content['consumer_secret'],
                     json_content['access_token'], json_content['access_token_secret'])
        content_object.put(Body=json.dumps(json_content))
        since_id = json_content["since_id"]
        since_id = bot.check_mentions(api, ["#"], since_id)
        json_content["since_id"] = since_id
        json_content["locked"] = False
        content_object.put(Body=json.dumps(json_content))
        logger.info(f'since id: {since_id}')
        return {'statusCode': 200,
                'body': json.dumps(json.dumps('success'))
                }

