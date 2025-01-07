import boto3 #type: ignore
import bcrypt #type: ignore
from botocore.exceptions import ClientError #type: ignore

# Initialize DynamoDB
dynamodb = boto3.resource('dynamodb', region_name='ap-southeast-3')  # Replace 'your-region' with your actual region
users_table = dynamodb.Table('Central_DB')  # Replace with the actual name of your DynamoDB table

def create_personal_database_table(username):
    try:
        # Define the table name based on username
        table_name = f"{username}_PersonalDB"
        
        # Create a new table with the specified schema
        table = dynamodb.create_table(
            TableName=table_name,
            KeySchema=[
                {'AttributeName': 'id', 'KeyType': 'HASH'},  # Partition key
                {'AttributeName': 'Product_id', 'KeyType': 'RANGE'}  # Sort key
            ],
            AttributeDefinitions=[
                {'AttributeName': 'id', 'AttributeType': 'S'},  # Partition key
                {'AttributeName': 'Product_id', 'AttributeType': 'S'}  # Sort key
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )
        
        # Wait for the table to be created
        table.meta.client.get_waiter('table_exists').wait(TableName=table_name)
        print(f"Personal database '{table_name}' created successfully for {username}.")
        
        return table_name
    except ClientError as e:
        print(f"Error creating personal database for {username}: {e}")
        return None

def register_user(username, password):
    # Hash the password
    password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    try:
        # Add the user to the central database
        users_table.put_item(
            Item={
                'Username': username,
                'PasswordHash': password_hash,
                'DatabaseName': f"{username}_PersonalDB"  # Set the name for the personal database
            },
            ConditionExpression='attribute_not_exists(Username)'  # Ensure username is unique
        )
        
        # Create a personal database for the user
        personal_db_name = create_personal_database_table(username)
        if personal_db_name:
            return {
                'status': 'success',
                'message': f"User registered and personal database '{personal_db_name}' created successfully."
            }
        else:
            return {
                'status': 'failure',
                'message': "User registered, but there was an issue creating the personal database."
            }
    except ClientError as e:
        if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
            return {
                'status': 'failure',
                'message': "Username already exists."
            }
        else:
            return {
                'status': 'failure',
                'message': f"Error registering user: {e}"
            }

