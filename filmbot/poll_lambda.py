import boto3
import json
import bot

REGION = 'us-west-1'
QUEUE = 'what-to-watch-queue'


def lambda_handler(event, context):
    s3 = boto3.resource('s3')
    content_object = s3.Object('aws-what-to-watch-json', 'bot.json')
    file_content = content_object.get()['Body'].read().decode('utf-8')
    json_content = json.loads(file_content)
    acc_num = json_content['acc_num']
    queue_url = f'https://sqs.{REGION}/{acc_num}/{QUEUE}'
    api = bot.config(json_content['consumer_key'], json_content['consumer_secret'],
                     json_content['access_token'], json_content['access_token_secret'])
    since_id = json_content["since_id"]
    since_id, mentions = bot.check_mentions(api, ["#"], since_id)
    json_content["since_id"] = since_id
    content_object.put(Body=json.dumps(json_content))
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