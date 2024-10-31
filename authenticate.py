import boto3 #type: ignore
import bcrypt #type: ignore
from botocore.exceptions import ClientError #type: ignore

# Initialize DynamoDB (same as in register_user)
dynamodb = boto3.resource('dynamodb', region_name='ap-southeast-3')  # Replace 'your-region' with your AWS region
users_table = dynamodb.Table('Central_DB')  # Replace with the actual name of your DynamoDB table

def authenticate_user(username, password):
    try:
        # Fetch the user record from the DynamoDB table
        response = users_table.get_item(Key={'Username': username})
        user = response.get('Item')
        
        # If the user exists, verify the password
        if user and bcrypt.checkpw(password.encode('utf-8'), user['PasswordHash'].encode('utf-8')):
            print("Authentication successful.")
            return user['DatabaseName']  # Return the associated database name for further use
        else:
            print("Authentication failed.")
            return None
    except ClientError as e:
        print("Error authenticating user:", e)
        return None
    
# # Example usage
# db_name = authenticate_user("test_user", "secure_password123")
# if db_name:
#     print(f"Authenticated! Access to user's personal database: {db_name}")
# else:
#     print("Authentication failed.")
    
