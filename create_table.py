import boto3
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize the AWS Resource
db = boto3.resource(
    'dynamodb',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY'),
    aws_secret_access_key=os.getenv('AWS_SECRET_KEY'),
    region_name='us-east-1'
)

try:
    table = db.create_table(
        TableName='AI_Database_Manager',
        KeySchema=[{'AttributeName': 'db_id', 'KeyType': 'HASH'}],
        AttributeDefinitions=[{'AttributeName': 'db_id', 'AttributeType': 'S'}],
        ProvisionedThroughput={'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
    )
    print("Table is being created. Please wait...")
    table.wait_until_exists()
    print("Table 'AI_Database_Manager' is now ACTIVE in AWS.")
except Exception as e:
    print(f"Error creating table: {e}")