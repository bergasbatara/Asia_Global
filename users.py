import boto3 #type: ignore
import bcrypt #type: ignore
from botocore.exceptions import ClientError #type: ignore

# Initialize DynamoDB
dynamodb = boto3.resource('dynamodb', region_name='ap-southeast-3')  # Replace 'your-region' with your actual region
users_table = dynamodb.Table('Central_DB')  # Replace with the actual name of your DynamoDB table

def register_user(username, password, database_name):
    # Hash the password
    password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    # Add the user to the DynamoDB Users table
    try:
        users_table.put_item(
            Item={
                'Username': username,
                'PasswordHash': password_hash,
                'DatabaseName': database_name
            },
            ConditionExpression='attribute_not_exists(Username)'  # Ensure the username is unique
        )
        print("User registered successfully.")
    except ClientError as e:
        if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
            print("Username already exists.")
        else:
            print("Error registering user:", e)

# Example usage
register_user("test_user", "secure_password123", "User1Database")