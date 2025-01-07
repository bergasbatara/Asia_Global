import boto3 #type: ignore
from botocore.exceptions import ClientError #type: ignore

# Initialize DynamoDB (you can reuse the same resource from earlier)
dynamodb = boto3.resource('dynamodb', region_name='ap-southeast-3')  # Replace 'your-region' with your AWS region

def connect_to_personal_database(database_name):
    """
    Connects to the specified personal database (DynamoDB table) for a user.
    
    Parameters:
    - database_name: str - The name of the DynamoDB table associated with the user.
    
    Returns:
    - DynamoDB Table resource if the table exists; otherwise, None.
    """
    try:
        # Connect to the user's personal database table
        personal_db = dynamodb.Table(database_name)
        
        # Perform a simple check to see if the table exists
        personal_db.load()  # This will raise an exception if the table does not exist
        
        return personal_db
    except ClientError as e:
        print(f"Error connecting to {database_name}: {e}")
        return None  # Return None if there’s an error

# # First, authenticate the user
# db_name = authenticate_user("test_user", "secure_password123")

# # If authentication is successful, connect to the user's personal database
# if db_name:
#     user_db = connect_to_personal_database(db_name)
#     if user_db:
#         # Now you can perform actions on the user's personal database (e.g., fetch, update data)
#         # Example: Fetch all items from the user's database
#         response = user_db.scan()
#         print("User's data:", response['Items'])
# else:
#     print("Authentication failed or database connection issue.")