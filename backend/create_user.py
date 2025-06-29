from passlib.context import CryptContext
import boto3

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('UsersTable')

def create_user(username, password, is_admin=False):
    hashed = pwd_context.hash(password)
    table.put_item(Item={
        'user_id': username,
        'hashed_password': hashed,
        'is_admin': is_admin
    })

# Usage:
# create_user("alice", "secret", True)
# create_user("bob", "password123", False)
