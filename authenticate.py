import boto3 #type: ignore
import bcrypt #type: ignore
from botocore.exceptions import ClientError #type: ignore

# Initialize DynamoDB (same as in register_user)
dynamodb = boto3.resource('dynamodb', region_name='ap-southeast-3')  # Replace 'your-region' with your AWS region
users_table = dynamodb.Table('Central_DB')  # Replace with the actual name of your DynamoDB table

def authenticate_user(username, password):
    # Fetch the user record from DynamoDB
    try:
        response = users_table.get_item(Key={'Username': username})
        user = response.get('Item')
        
        if user and bcrypt.checkpw(password.encode('utf-8'), user['PasswordHash'].encode('utf-8')):
            # Authentication successful
            return {
                'status': 'success',
                'message': 'Authentication successful.',
                'database_name': user['DatabaseName']  # Assuming 'DatabaseName' is stored for each user
            }
        else:
            # Authentication failed
            return {
                'status': 'failure',
                'message': 'Invalid username or password.'
            }
    except ClientError as e:
        # Handle DynamoDB error
        return {
            'status': 'failure',
            'message': f"Error accessing database: {e}"
        }
    
# # Example usage
# db_name = authenticate_user("test_user", "secure_password123")
# if db_name:
#     print(f"Authenticated! Access to user's personal database: {db_name}")
# else:
#     print("Authentication failed.")
    
