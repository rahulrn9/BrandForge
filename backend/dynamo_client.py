import boto3

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

def store_content(user_id, content, metadata):
    table = dynamodb.Table('ContentTable')
    from datetime import datetime
    table.put_item(Item={
        'user_id': user_id,
        'timestamp': datetime.utcnow().isoformat(),
        'content': content,
        'metadata': metadata
    })

def log_event(user_id, event_type, metadata):
    table = dynamodb.Table('AnalyticsTable')
    table.put_item(Item={
        'user_id': user_id,
        'event_type': event_type,
        'timestamp': metadata.get("timestamp"),
        'metadata': metadata
    })

def assign_ab_variant(user_id):
    return "A" if hash(user_id) % 2 == 0 else "B"
